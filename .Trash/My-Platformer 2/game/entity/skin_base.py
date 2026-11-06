import pygame

class SkinBase:
    def __init__(self, skin_png):

        self.SCALE_FACTOR: int = 16
        self.skin_png = pygame.transform.scale(
            skin_png, (8 * self.SCALE_FACTOR, 4 * self.SCALE_FACTOR)
        )

        self.body_part_imgs = {
            'body': {
                -1: self._crop_skin(56,40,8,24),
                1: self._crop_skin(32,40,8,24)
            },
            'leg': {
                -1: {
                    -1: self._crop_skin(0,40,8,24),
                    1: self._crop_skin(8,40,8,24)
                },
                1: {
                    -1: self._crop_skin(24,40,8,24),
                    1: self._crop_skin(16,40,8,24)
                }
            },
            'arm': {
                -1: {
                    -1: self._crop_skin(80,40,8,24),
                    1: self._crop_skin(88,40,8,24)
                },
                1: {
                    -1: self._crop_skin(104,40,8,24),
                    1: self._crop_skin(96,40,8,24)
                }
            },
            'head': {
                -1: self._crop_skin(32,16,16,16),
                1: self._crop_skin(0,16,16,16)
            }
        }

    def draw_body(self, screen, direction: str, midbottom: tuple) -> None:

        body = self.body_part_imgs['body'][direction]
        body_rect = body.get_rect()
        body_rect.midbottom = midbottom

        screen.blit(body, body_rect)

    def draw_head(
        self, screen, direction: str, midbottom: tuple, angle: float=None
    ) -> None:

        head = self.body_part_imgs['head'][direction]
        pivot = pygame.Vector2(head.get_width() / 2, head.get_height())
        new_head, new_rect = self._rotate_img(head, midbottom, pivot, angle)
        screen.blit(new_head, new_rect)

    def draw_arm(
        self, screen, side: str, direction: str, midtop: tuple, angle: float=0
    ) -> None:

        arm = self.body_part_imgs['arm'][side][direction]

        if round(angle) != 0:
            pivot = pygame.Vector2(arm.get_width() / 2, 4)
            anchorx, anchory = midtop
            anchory += 4
            anchor = (anchorx, anchory)
            new_arm, new_rect = self._rotate_img(arm, anchor, pivot, angle)
        else:
            new_arm, new_rect = arm, arm.get_rect()
            new_rect.midtop = midtop

        screen.blit(new_arm, new_rect)

    def draw_leg(
        self, screen, side: str, direction: str, midtop: tuple, angle: float=0
    ) -> None:

        leg = self.body_part_imgs['leg'][side][direction]

        if round(angle) != 0:
            pivot = pygame.Vector2(leg.get_width() / 2, 0)
            new_leg, new_rect = self._rotate_img(leg, midtop, pivot, angle)
        else:
            new_leg, new_rect = leg, leg.get_rect()
            new_rect.midtop = midtop

        screen.blit(new_leg, new_rect)

    def _crop_skin(self, x: int, y: int, width: int, height: int):
        return self.skin_png.subsurface(pygame.Rect(x, y, width, height))

    def _rotate_img(
        self, original_img, anchor: tuple, 
        pivot_vect: pygame.Vector2, angle: float=None
    ):

        center = pygame.Vector2(
            original_img.get_width() / 2, original_img.get_height() / 2
        )
        pivot = pivot_vect

        pivot_offset = pivot - center
        rotated_offset = pivot_offset.rotate(-angle)
        rot_img = pygame.transform.rotate(original_img, angle)

        new_rect = rot_img.get_rect()
        new_rect.center = pygame.Vector2(anchor) - rotated_offset

        return (rot_img, new_rect)
