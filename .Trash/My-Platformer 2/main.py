import pygame
from renderer.game_renderer import GameRenderer
from game.game import Game
from game.world.world import World
from renderer.camera import Camera

pygame.init()
screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
clock = pygame.time.Clock()

world_seed = 6129

camera = Camera()
world = World(world_seed)
game = Game(world, camera, world_seed)
renderer = GameRenderer(screen, game, world, camera)

running = True

# Implement ability to zoom in or out!
# Add actual max/min y world boundaries (stop chunk generation there)!

while running:

    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    game.progress(keys, mouse_buttons, dt)

    renderer.fps = int(clock.get_fps())
    renderer.draw(dt)

    pygame.display.flip()

pygame.quit()