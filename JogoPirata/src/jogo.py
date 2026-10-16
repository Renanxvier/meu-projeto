import pygame
import random
import sys

# ==========================================
# 1. INICIALIZAÇÃO GERAL (Roda só uma vez)
# ==========================================
pygame.init()
pygame.font.init()
pygame.mixer.init()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Jogo Principal")

BRANCO = (255, 255, 255)
VERMELHO = (255, 50, 50)
AMARELO = (255, 255, 0)
LARANJA = (255, 165, 0)
PRETO = (0, 0, 0)

relogio = pygame.time.Clock()
FPS = 60

# Fontes
fonte_pontos = pygame.font.SysFont(None, 40)
fonte_grande = pygame.font.SysFont(None, 80)
fonte_zoeira = pygame.font.SysFont(None, 60)

# ==========================================
# 2. CARREGAMENTO DE ASSETS (Imagens e Sons)
# ==========================================
tamanho_jogador = 80
tamanho_inimigo = 70
tamanho_rum = 40

try:
    img_fundo = pygame.image.load('navio.jpg').convert()
    img_fundo = pygame.transform.scale(img_fundo, (LARGURA, ALTURA))

    img_jogador = pygame.image.load('pirata.png').convert_alpha()
    img_jogador = pygame.transform.scale(
        img_jogador, (tamanho_jogador, tamanho_jogador))

    img_inimigo = pygame.image.load('inimigo.png').convert_alpha()
    img_inimigo = pygame.transform.scale(
        img_inimigo, (tamanho_inimigo, tamanho_inimigo))

    img_faca = pygame.image.load('faca.png').convert_alpha()
    img_faca = pygame.transform.scale(img_faca, (20, 45))

    img_caveira = pygame.image.load('caveira.png').convert_alpha()
    img_caveira = pygame.transform.scale(img_caveira, (40, 40))

    img_rum = pygame.image.load('rum.png').convert_alpha()
    img_rum = pygame.transform.scale(img_rum, (tamanho_rum, tamanho_rum))
except Exception as erro:
    print(f"ERRO: Faltou alguma imagem! Detalhe: {erro}")
    pygame.quit()
    sys.exit()

tem_som_dano = True
try:
    som_dano = pygame.mixer.Sound('dano.wav')
except:
    tem_som_dano = False

pelicula = pygame.Surface((LARGURA, ALTURA))
pelicula.fill((0, 0, 0))
pelicula.set_alpha(120)

MARGEM_ESQUERDA = 120
MARGEM_DIREITA = LARGURA - 120

# ==========================================
# 3. A FASE BÔNUS (Empacotada em uma Função)
# ==========================================


def jogar_fase_bonus():
    """
    Roda a fase bônus por 30 segundos.
    Retorna a quantidade de pontos que o jogador conseguiu.
    """
    jogador_x = LARGURA // 2
    jogador_y = ALTURA - tamanho_jogador - 10
    velocidade_jogador = 7
    vidas = 3
    pontos = 0

    tempo_bebado = 0
    cooldown_faca = 0
    tempo_zoeira = 0
    mensagem_zoeira = ""

    facas = []
    velocidade_faca = 10
    inimigos = []
    velocidade_inimigo = 4
    timer_inimigo = 0
    canecas = []
    velocidade_rum = 2

    # --- NOVIDADE: Timer da Fase Bônus (30 segundos) ---
    frames_totais = FPS * 30

    rodando_bonus = True
    while rodando_bonus:
        tela.blit(img_fundo, (0, 0))
        tela.blit(pelicula, (0, 0))

        # Diminui o tempo da fase
        frames_totais -= 1
        if frames_totais <= 0:
            return pontos  # O tempo acabou! Devolve os pontos e sai da fase.

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and cooldown_faca == 0:
                    nova_faca = pygame.Rect(
                        jogador_x + tamanho_jogador // 2 - 10, jogador_y, 20, 45)
                    facas.append(nova_faca)
                    cooldown_faca = 10

        # Temporizadores
        if cooldown_faca > 0:
            cooldown_faca -= 1
        if tempo_zoeira > 0:
            tempo_zoeira -= 1
        if tempo_bebado > 0:
            tempo_bebado -= 1

        # Movimentação
        teclas = pygame.key.get_pressed()
        if tempo_bebado > 0:
            if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jogador_x < MARGEM_DIREITA - tamanho_jogador:
                jogador_x += velocidade_jogador
            if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jogador_x > MARGEM_ESQUERDA:
                jogador_x -= velocidade_jogador
        else:
            if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jogador_x > MARGEM_ESQUERDA:
                jogador_x -= velocidade_jogador
            if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jogador_x < MARGEM_DIREITA - tamanho_jogador:
                jogador_x += velocidade_jogador

        # Gerar Inimigos e Rum
        timer_inimigo += 1
        if timer_inimigo > 30:
            posicao_x = random.randint(
                MARGEM_ESQUERDA, MARGEM_DIREITA - tamanho_inimigo)
            inimigos.append(pygame.Rect(
                posicao_x, -tamanho_inimigo, tamanho_inimigo, tamanho_inimigo))
            timer_inimigo = 0

        if random.randint(1, 300) == 1:
            pos_x_rum = random.randint(
                MARGEM_ESQUERDA, MARGEM_DIREITA - tamanho_rum)
            canecas.append(pygame.Rect(
                pos_x_rum, -tamanho_rum, tamanho_rum, tamanho_rum))

        # Atualizar Facas
        for faca in facas[:]:
            faca.y -= velocidade_faca
            if faca.y < 0:
                facas.remove(faca)
                if pontos > 0:
                    pontos -= 2
                    if pontos <= 0:
                        pontos = 0
                        mensagem_zoeira = "MARUJO VESGO! ZEROU OS PONTOS!"
                        tempo_zoeira = 90

        jogador_rect = pygame.Rect(
            jogador_x, jogador_y, tamanho_jogador, tamanho_jogador)

        # Atualizar Rum
        for caneca in canecas[:]:
            caneca.y += velocidade_rum
            if caneca.y > ALTURA:
                canecas.remove(caneca)
                continue
            if caneca.colliderect(jogador_rect):
                canecas.remove(caneca)
                if vidas < 3:
                    vidas += 1
                tempo_bebado = FPS * 5
                continue
            for faca in facas[:]:
                if caneca.colliderect(faca):
                    canecas.remove(caneca)
                    facas.remove(faca)
                    break

        # Atualizar Inimigos e Colisões
        for inimigo in inimigos[:]:
            inimigo.y += velocidade_inimigo
            if inimigo.colliderect(jogador_rect) or inimigo.y > ALTURA:
                vidas -= 1
                if tem_som_dano:
                    som_dano.play()
                inimigos.remove(inimigo)
                continue
            for faca in facas[:]:
                if inimigo.colliderect(faca):
                    inimigos.remove(inimigo)
                    facas.remove(faca)
                    pontos += 10
                    break

        # Condição de Derrota
        if vidas <= 0:
            return 0  # Se morrer na fase bônus, perde todos os pontos ganhos nela e volta pro jogo principal

        # Desenhar Personagens
        tela.blit(img_jogador, (jogador_x, jogador_y))
        for faca in facas:
            tela.blit(img_faca, (faca.x, faca.y))
        for inimigo in inimigos:
            tela.blit(img_inimigo, (inimigo.x, inimigo.y))
        for caneca in canecas:
            tela.blit(img_rum, (caneca.x, caneca.y))

        # Interface Visual
        if tempo_bebado > 0:
            texto_bebado = fonte_pontos.render(
                "CONTROLES INVERTIDOS!", True, AMARELO)
            tela.blit(texto_bebado, (LARGURA // 2 -
                      texto_bebado.get_width() // 2, ALTURA - 50))

        if tempo_zoeira > 0:
            texto_zombaria = fonte_zoeira.render(
                mensagem_zoeira, True, LARANJA)
            tela.blit(texto_zombaria, (LARGURA // 2 -
                      texto_zombaria.get_width() // 2, ALTURA // 2 - 100))

        # HUD: Pontos, Vidas e Tempo Restante
        texto_pontos = fonte_pontos.render(
            f"Pontos Bônus: {pontos}", True, BRANCO)
        tela.blit(texto_pontos, (10, 10))

        segundos_restantes = frames_totais // FPS
        texto_tempo = fonte_pontos.render(
            f"Tempo: {segundos_restantes}s", True, AMARELO)
        tela.blit(texto_tempo, (LARGURA // 2 -
                  texto_tempo.get_width() // 2, 10))

        for i in range(vidas):
            posicao_x_caveira = LARGURA - 50 - (i * 45)
            tela.blit(img_caveira, (posicao_x_caveira, 10))

        pygame.display.flip()
        relogio.tick(FPS)


# ==========================================
# 4. O JOGO PRINCIPAL
# ==========================================
pontuacao_total_do_jogo = 0

rodando_jogo_principal = True
while rodando_jogo_principal:
    tela.fill(PRETO)

    # Textos do "Menu/Jogo Principal"
    texto_titulo = fonte_grande.render("O GRANDE JOGO PRINCIPAL", True, BRANCO)
    texto_info = fonte_pontos.render(
        f"Sua Pontuação Total: {pontuacao_total_do_jogo}", True, AMARELO)
    texto_instrucao = fonte_pontos.render(
        "Aperte 'B' para entrar na FASE BÔNUS", True, BRANCO)

    tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 150))
    tela.blit(texto_info, (LARGURA // 2 - texto_info.get_width() // 2, 250))
    tela.blit(texto_instrucao, (LARGURA // 2 -
              texto_instrucao.get_width() // 2, 350))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando_jogo_principal = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_b:
                # --- A MÁGICA ACONTECE AQUI ---
                # Pausa o jogo principal, roda a fase bônus, e pega os pontos quando ela terminar!
                pontos_da_fase = jogar_fase_bonus()
                pontuacao_total_do_jogo += pontos_da_fase

    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
sys.exit()
