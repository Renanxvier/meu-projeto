import pygame

# Inicializa o Pygame
pygame.init()

# Cria uma tela invisível de 40x40 pixels com fundo transparente
tamanho = 40
imagem = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Desenha o crânio (Parte de cima)
pygame.draw.rect(imagem, BRANCO, (5, 5, 30, 20))
# Desenha a mandíbula (Parte de baixo)
pygame.draw.rect(imagem, BRANCO, (10, 25, 20, 10))

# Desenha os Olhos (Pretos)
pygame.draw.rect(imagem, PRETO, (10, 12, 8, 8))
pygame.draw.rect(imagem, PRETO, (22, 12, 8, 8))

# Desenha o Nariz
pygame.draw.rect(imagem, PRETO, (18, 20, 4, 4))

# Desenha as linhas dos Dentes
pygame.draw.rect(imagem, PRETO, (14, 28, 2, 7))
pygame.draw.rect(imagem, PRETO, (19, 28, 2, 7))
pygame.draw.rect(imagem, PRETO, (24, 28, 2, 7))

# Salva o desenho como um arquivo .png
pygame.image.save(imagem, "caveira.png")
print("Sucesso! O arquivo 'caveira.png' foi criado na sua pasta.")

pygame.quit()