import pygame

pygame.init()
tamanho = 40
imagem = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)

MARROM = (139, 69, 19)
AMARELO = (255, 215, 0)
CINZA = (200, 200, 200)

# Desenha o copo de madeira (Marrom)
pygame.draw.rect(imagem, MARROM, (8, 10, 20, 25))
# Desenha a alça da caneca
pygame.draw.rect(imagem, MARROM, (28, 15, 8, 15), 3)
# Desenha a espuma do rum transbordando (Amarelo/Branco)
pygame.draw.circle(imagem, AMARELO, (12, 10), 6)
pygame.draw.circle(imagem, AMARELO, (22, 10), 6)
pygame.draw.circle(imagem, CINZA, (17, 8), 7)

pygame.image.save(imagem, "rum.png")
print("Sucesso! O arquivo 'rum.png' foi criado.")
pygame.quit()