import pygame
import os

pygame.init()

os.makedirs("assets", exist_ok=True)

TILE_SIZE = 32

image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

# ぼんの体
pygame.draw.circle(image, (230, 180, 120), (16, 17), 10)

# 耳
pygame.draw.polygon(image, (230, 180, 120), [(8, 10), (12, 2), (16, 10)])
pygame.draw.polygon(image, (230, 180, 120), [(16, 10), (20, 2), (24, 10)])

# 顔
pygame.draw.circle(image, (0, 0, 0), (13, 16), 2)
pygame.draw.circle(image, (0, 0, 0), (19, 16), 2)
pygame.draw.circle(image, (80, 40, 20), (16, 20), 2)

pygame.image.save(image, "assets/bon.png")

print("assets/bon.png を作りました！")