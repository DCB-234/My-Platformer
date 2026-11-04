import math
import random

class CaveGenerator:
    def __init__(self, world_seed, terrain_generator):
        self.terrain_generator = terrain_generator

        self.world_seed = world_seed
        self.CHUNK_SIZE = 16

        # Cave generation settings
        self.WORMS_PER_CHUNK = 2
        self.WORM_CHANCE = 0.06
        self.MIN_LENGTH = 30
        self.MAX_LENGTH = 80
        self.MIN_RADIUS = 2.0
        self.MAX_RADIUS = 2.5
        self.BRANCH_CHANCE = 0.05
        self.MAX_TURN = 0.25
        self.TURN_SCALE = 15.0

        # Depth & Surface clamping settings
        self.MAX_DEPTH = 256
        self.BOTTOM_TAPER_ZONE = 40.0
        self.SURFACE_TAPER_ZONE = 30.0

        self.ENTRANCE_CHANCE = 0.1
        self.ENTRANCE_AIR_LIMIT = 15.0

    def chunk_seed(self, world_seed, chunk_x, chunk_y):
        return (world_seed ^ (chunk_x * 341873128712) ^ (chunk_y * 132897987541)) & 0xFFFFFFFF

    def carve_circle(self, chunk_grid, x, y, radius, c_min_x, c_max_x, c_min_y, c_max_y):
        effective_max_y = min(self.MAX_DEPTH, c_max_y)
        
        min_y = max(math.ceil(y - radius), c_min_y)
        max_y = min(math.floor(y + radius), effective_max_y - 1)
      
        if min_y > max_y:
            return

        radius_sq = radius * radius
        for block_y in range(min_y, max_y + 1):
            dy = block_y - y
            dy_sq = dy * dy
          
            rem_sq = radius_sq - dy_sq
            if rem_sq < 0:
                continue
              
            rem = math.sqrt(rem_sq)
          
            row_min_x = max(math.ceil(x - rem), c_min_x)
            row_max_x = min(math.floor(x + rem), c_max_x - 1)
          
            if row_min_x <= row_max_x:
                start_idx = row_min_x - c_min_x
                end_idx = row_max_x - c_min_x + 1
              
                chunk_grid[block_y - c_min_y][start_idx:end_idx] = [True] * (end_idx - start_idx)

    def smooth_noise_1d(self, x, seed_offset):
        x0 = int(x)
        t = x - x0
        t = t * t * (3.0 - 2.0 * t)
      
        n0 = x0 * 374761393 + seed_offset
        v0_temp = (n0 ^ (n0 >> 13)) * 1274126177
        v0 = (v0_temp ^ (v0_temp >> 16)) & 0xFFFFFFFF
      
        n1 = n0 + 374761393
        v1_temp = (n1 ^ (n1 >> 13)) * 1274126177
        v1 = (v1_temp ^ (v1_temp >> 16)) & 0xFFFFFFFF
      
        return (v0 + (v1 - v0) * t) / 4294967295.0

    def generate_worm(self, chunk_grid, x, y, angle, length, worm_seed, radius, c_min_x, c_max_x, c_min_y, c_max_y, is_entrance, depth=0):
        worm_rng = random.Random(worm_seed)
      
        inv_turn_scale = 1.0 / self.TURN_SCALE
        max_turn_multiplier = self.MAX_TURN * 2.0
        max_turn_subtractor = self.MAX_TURN
      
        seed_offset = worm_seed * 1442695041

        for step in range(length):
            if y >= self.MAX_DEPTH:
                break
                
            dist_to_bottom = self.MAX_DEPTH - y
            if dist_to_bottom <= 0:
                break
              
            bottom_taper = max(0.0, min(1.0, dist_to_bottom / self.BOTTOM_TAPER_ZONE))
          
            surface_y = self.terrain_generator.get_terrain_height(x)
            dist_to_surface = y - surface_y

            if is_entrance:
                if dist_to_surface <= -self.ENTRANCE_AIR_LIMIT:
                    break
              
                if dist_to_surface < 0:
                    surface_taper = max(0.0, 1.0 - (abs(dist_to_surface) / self.ENTRANCE_AIR_LIMIT))
                else:
                    surface_taper = 1.0
            else:
                if dist_to_surface <= 0:
                    break
                surface_taper = max(0.0, min(1.0, dist_to_surface / self.SURFACE_TAPER_ZONE))

            taper_multiplier = min(bottom_taper, surface_taper)

            current_radius = radius * taper_multiplier
            padded_r = current_radius + 1.0

            if current_radius >= 0.5:
                if c_min_x - padded_r <= x < c_max_x + padded_r and c_min_y - padded_r <= y < c_max_y + padded_r:
                    self.carve_circle(chunk_grid, x, y, current_radius, c_min_x, c_max_x, c_min_y, c_max_y)
          
            turn = self.smooth_noise_1d(step * inv_turn_scale, seed_offset)
            angle += (turn * max_turn_multiplier) - max_turn_subtractor

            x += math.cos(angle)
            y += math.sin(angle)

            if depth < 2 and worm_rng.random() < self.BRANCH_CHANCE:
                branch_length = worm_rng.randint(15, 40)
                branch_radius = radius * 0.8
                branch_angle = angle + worm_rng.choice((-1, 1)) * worm_rng.uniform(0.5, 1.0)
                branch_seed = worm_rng.getrandbits(32)
              
                max_branch_reach = branch_length + (40 if depth == 0 else 0) + branch_radius

                if not (x + max_branch_reach < c_min_x or x - max_branch_reach >= c_max_x or
                        y + max_branch_reach < c_min_y or y - max_branch_reach >= c_max_y):

                    self.generate_worm(
                        chunk_grid, x, y, branch_angle, branch_length,
                        branch_seed, branch_radius, c_min_x, c_max_x, c_min_y, c_max_y, is_entrance, depth + 1
                    )

    def generate_cave_chunk(self, chunk_x, chunk_y):
        chunk_grid = [[False] * self.CHUNK_SIZE for _ in range(self.CHUNK_SIZE)]
        chunk_min_y = chunk_y * self.CHUNK_SIZE

        if chunk_min_y >= self.MAX_DEPTH:
            return chunk_grid

        search_radius = 5
        chunk_size = self.CHUNK_SIZE
     
        chunk_min_x = chunk_x * chunk_size
        chunk_max_x = chunk_min_x + chunk_size
        chunk_max_y = chunk_min_y + chunk_size

        worm_chance = self.WORM_CHANCE
        worms_per_chunk = self.WORMS_PER_CHUNK

        for source_y in range(chunk_y - search_radius, chunk_y + search_radius + 1):
            for source_x in range(chunk_x - search_radius, chunk_x + search_radius + 1):
                source_seed = self.chunk_seed(self.world_seed, source_x, source_y)
                rng = random.Random(source_seed)

                if rng.random() > worm_chance:
                    continue

                for _ in range(worms_per_chunk):
                    start_x = source_x * chunk_size + rng.randrange(chunk_size)
                    start_y = source_y * chunk_size + rng.randrange(chunk_size)
                    
                    if start_y >= self.MAX_DEPTH:
                        continue

                    angle = rng.uniform(0, math.tau)
                    length = rng.randint(self.MIN_LENGTH, self.MAX_LENGTH)
                    radius = rng.uniform(self.MIN_RADIUS, self.MAX_RADIUS)
                    worm_seed = rng.getrandbits(32)
                 
                    is_entrance = rng.random() < self.ENTRANCE_CHANCE
                 
                    max_reach = length + 80 + radius
                 
                    if (start_x + max_reach < chunk_min_x or start_x - max_reach >= chunk_max_x or
                        start_y + max_reach < chunk_min_y or start_y - max_reach >= chunk_max_y):
                        continue


                    self.generate_worm(
                        chunk_grid, start_x, start_y, angle, length, worm_seed,
                        radius, chunk_min_x, chunk_max_x, chunk_min_y, chunk_max_y, is_entrance
                    )

        return chunk_grid