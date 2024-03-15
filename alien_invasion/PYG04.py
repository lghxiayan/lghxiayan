import pygame, sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pygame事件处理")
fps = 1
fclock = pygame.time.Clock()
num = 1

while True:
    uevent = pygame.event.Event(pygame.KEYDOWN, {"unicode": 123, "key": pygame.K_SPACE, "mod": pygame.KMOD_ALT})
    pygame.event.post(uevent)
    num += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.unicode == "":
                print(f"[KEYDOWN {num}]:", "#", event.key, event.mod)
            else:
                print(f"[KEYDOWN {num}]:", event.unicode, event.key, event.mod)
        # elif event.type == pygame.MOUSEMOTION:
        #     print("[MOUSEMOTION]:", event.pos, event.rel, event.buttons)
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     print("[MOUSEBUTTONUP]:", event.pos, event.button)
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     print("[MOUSEBUTTONDOWN]:", event.pos, event.button)

    pygame.display.update()
    fclock.tick(fps)
