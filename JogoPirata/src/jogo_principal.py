import pygame
import sys
import random
import math
import os
import ctypes

try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

# Inicialização forçada do mixer com parâmetros específicos para garantir o áudio no .exe
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
pygame.font.init()

LARGURA = 800
ALTURA = 600
is_fullscreen = False
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Mutiny Tactics - Edição Polida Top-Down")

# Paleta de Cores Aprimorada
BRANCO = (245, 245, 245)
PRETO = (20, 20, 20)
CINZA_ESCURO = (45, 45, 55)
CINZA_CLARO = (180, 180, 190)
CINZA_SUTIL = (80, 80, 95)
VERMELHO_BANDANA = (220, 40, 40)

AZUL_CAPITAO = (30, 100, 220)
CINZA_MARUJO = (120, 120, 130)
ROSA_MARUJA = (210, 60, 160)
AMARELO_OURO = (255, 215, 0)
LARANJA_FOGO = (255, 120, 30)
ROXO_MAGIA = (140, 40, 200)

MADEIRA_NAVIO = (139, 69, 19)
MADEIRA_CLARA = (165, 85, 30)
MADEIRA_ESCURA = (110, 50, 10)     
MADEIRA_SAFE = (115, 55, 15)      
AREIA_ILHA = (222, 184, 135)
AREIA_ESCURA = (200, 160, 110)    
AGUA_LAGOA = (60, 140, 200)       
AGUA_BORDA = (40, 100, 160)
PEDRA_ILHA = (105, 105, 105)
CAVERNA_FUNDO = (35, 35, 45)
CAVERNA_DETALHE = (25, 25, 35)    
ROCHA_CAVERNA = (70, 70, 85)
VERDE_SAIDA = (40, 200, 80)
COR_BARRIL = (90, 45, 10)        
COR_CORDA = (190, 160, 110)       

relogio = pygame.time.Clock()
FPS = 60

if getattr(sys, 'frozen', False):
    diretorio_assets = os.path.join(sys._MEIPASS, "assets")
else:
    diretorio_assets = os.path.join(os.path.dirname(__file__), "..", "assets")

try:
    fonte = pygame.font.SysFont("Georgia", 24, bold=True)
    fonte_grande = pygame.font.SysFont("Georgia", 48, bold=True)
    fonte_pequena = pygame.font.SysFont("Georgia", 16, bold=True)
except:
    fonte = pygame.font.SysFont("Arial", 22, bold=True)
    fonte_grande = pygame.font.SysFont("Arial", 45, bold=True)
    fonte_pequena = pygame.font.SysFont("Arial", 16, bold=True)

opcao_menu = 0
opcoes_lista = ["JOGAR", "COMO JOGAR", "OPÇÕES", "SAIR"]
opcao_config_menu = 0
opcao_pause = 0
opcoes_pause = ["CONTINUAR", "OPÇÕES", "MENU PRINCIPAL"]
estado_origem_opcoes = "MENU_INICIAL"

img_capitao = None
img_marujo = None
img_maruja = None
img_atirador = None
img_perseguidor = None

img_barril = None
img_coqueiro = None
img_cristal = None
som_dano = None

def carregar_e_ajustar_sprite(caminho, tamanho_alvo):
    if os.path.exists(caminho):
        surf_original = pygame.image.load(caminho).convert_alpha()
        surf_padrao = pygame.Surface((tamanho_alvo, tamanho_alvo), pygame.SRCALPHA)
        w_orig, h_orig = surf_original.get_size()
        fator = min(tamanho_alvo / w_orig, tamanho_alvo / h_orig)
        novo_w = int(w_orig * fator)
        novo_h = int(h_orig * fator)
        surf_redimensionada = pygame.transform.scale(surf_original, (novo_w, novo_h))
        pos_x = (tamanho_alvo - novo_w) // 2
        pos_y = (tamanho_alvo - novo_h) // 2
        surf_padrao.blit(surf_redimensionada, (pos_x, pos_y))
        return surf_padrao
    return None

try:
    img_capitao = carregar_e_ajustar_sprite(os.path.join(diretorio_assets, "capitão.png"), 45)
    img_marujo = carregar_e_ajustar_sprite(os.path.join(diretorio_assets, "marujo.png"), 64)
    img_maruja = carregar_e_ajustar_sprite(os.path.join(diretorio_assets, "maruja.png"), 50)
    
    caminho_base_ini = os.path.join(diretorio_assets, "maruja.png")
    if os.path.exists(caminho_base_ini):
        surf_ini_base = pygame.image.load(caminho_base_ini).convert_alpha()
        img_temp = pygame.transform.scale(surf_ini_base, (50, 50))
        img_atirador = pygame.transform.grayscale(img_temp)
        
        caminho_base_ini2 = os.path.join(diretorio_assets, "marujo.png")
        if os.path.exists(caminho_base_ini2):
            surf_ini_base2 = pygame.image.load(caminho_base_ini2).convert_alpha()
            img_temp2 = pygame.transform.scale(surf_ini_base2, (50, 50))
            img_perseguidor = pygame.transform.grayscale(img_temp2)
        else:
            img_perseguidor = img_atirador.copy()

    img_barril = carregar_e_ajustar_sprite(os.path.join(diretorio_assets, "barril.png"), 70)
    img_coqueiro = carregar_e_ajustar_sprite(os.path.join(diretorio_assets, "coqueiro.png"), 70)
    img_cristal = carregar_e_ajustar_sprite(os.path.join(diretorio_assets, "cristal.png"), 70)
    
    caminho_som_dano = os.path.join(diretorio_assets, "dano.wav")
    if os.path.exists(caminho_som_dano):
        som_dano = pygame.mixer.Sound(caminho_som_dano)
            
    print("Sucesso! Assets e sons carregados.")
except Exception as e:
    print(f"Erro ao processar os arquivos: {e}")

def tocar_musica_fase(fase):
    try:
        if fase == 1:
            caminho_musica = os.path.join(diretorio_assets, "musica_fase1.wav")
            if not os.path.exists(caminho_musica):
                caminho_musica = os.path.join(diretorio_assets, "musica_fase1.ogg")
        elif fase == 2:
            caminho_musica = os.path.join(diretorio_assets, "musica_fase2.wav")
        else:
            caminho_musica = os.path.join(diretorio_assets, "musica_fase3.wav")
            if not os.path.exists(caminho_musica):
                caminho_musica = os.path.join(diretorio_assets, "musica_fase3.mp3")

        if os.path.exists(caminho_musica):
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
    except Exception as e:
        print(f"Aviso ao carregar trilha sonora: {e}")

def criar_personagens_base():
    return [
        {"id": 0, "nome": "Capitão", "cor": AZUL_CAPITAO, "vel": 4, "tem_longe": True, "tem_perto": True, "cooldown_longe": 30, "cooldown_perto": 20, "vivo": True, "mortes": 0, "perdido_definitivo": False},
        {"id": 1, "nome": "Marujo", "cor": CINZA_MARUJO, "vel": 5, "tem_longe": False, "tem_perto": True, "cooldown_longe": 0, "cooldown_perto": 12, "vivo": False, "mortes": 0, "perdido_definitivo": False},
        {"id": 2, "nome": "Maruja", "cor": ROSA_MARUJA, "vel": 5, "tem_longe": True, "tem_perto": False, "cooldown_longe": 25, "cooldown_perto": 0, "vivo": False, "mortes": 0, "perdido_definitivo": False}
    ]

personagens = criar_personagens_base()
equipe_liberada = [0] 
equipe_selecionada = [0] 
historico_posicoes = [] 

indice_atual = 0 
jogador_x = LARGURA // 2
jogador_y = ALTURA - 80
tamanho_jogador = 50
direcao_olhar = (0, -1) 

tiros_jogador = [] 
golpes_espada = [] 
tiros_inimigos = [] 

cooldown_atual_longe = 0
cooldown_atual_perto = 0

pontos = 0
vidas_gerais = 3 
fase_atual = 1 
bonus_limpeza_concluido = False

zona_saida = pygame.Rect(300, 0, 200, 40)
safe_zone = pygame.Rect(250, ALTURA - 110, 300, 65) 
zona_agua_praia = pygame.Rect(120, 220, 180, 110) 
membros_caidos = []

def criar_paredes_fase(fase):
    return [
        pygame.Rect(0, 40, 300, 20),            
        pygame.Rect(500, 40, LARGURA - 500, 20), 
        pygame.Rect(0, 40, 20, ALTURA - 40),    
        pygame.Rect(LARGURA - 20, 40, 20, ALTURA - 40), 
        pygame.Rect(0, ALTURA - 20, LARGURA, 20)      
    ]

def criar_obstaculos(fase):
    if fase == 1:
        return [
            pygame.Rect(240, 220, 70, 70), 
            pygame.Rect(450, 320, 70, 70), 
            pygame.Rect(130, 430, 70, 70),  
            pygame.Rect(600, 430, 70, 70)   
        ]
    elif fase == 2:
        return [
            pygame.Rect(220, 200, 70, 70),
            pygame.Rect(520, 200, 70, 70),
            pygame.Rect(350, 380, 70, 70)
        ]
    else:
        return [
            pygame.Rect(180, 200, 70, 70),
            pygame.Rect(580, 200, 70, 70),
            pygame.Rect(380, 220, 70, 70),
            pygame.Rect(300, 420, 70, 70)
        ]

def criar_inimigos(fase):
    if fase == 1:
        candidatos = [
            {"tipo": "atirador", "rect": pygame.Rect(200, 120, 50, 50), "cooldown": 60},
            {"tipo": "atirador", "rect": pygame.Rect(550, 120, 50, 50), "cooldown": 120},
            {"tipo": "perseguidor", "rect": pygame.Rect(400, 350, 50, 50), "dx": 0, "dy": 0, "tempo_mov": 0},
            {"tipo": "perseguidor", "rect": pygame.Rect(150, 350, 50, 50), "dx": 0, "dy": 0, "tempo_mov": 0}
        ]
    elif fase == 2:
        candidatos = [
            {"tipo": "atirador", "rect": pygame.Rect(100, 100, 50, 50), "cooldown": 40},
            {"tipo": "atirador", "rect": pygame.Rect(650, 100, 50, 50), "cooldown": 50},
            {"tipo": "perseguidor", "rect": pygame.Rect(100, 350, 50, 50), "dx": 0, "dy": 0, "tempo_mov": 0},
            {"tipo": "perseguidor", "rect": pygame.Rect(650, 350, 50, 50), "dx": 0, "dy": 0, "tempo_mov": 0},
            {"tipo": "atirador", "rect": pygame.Rect(400, 120, 50, 50), "cooldown": 60}
        ]
    else:
        candidatos = [
            {"tipo": "atirador", "rect": pygame.Rect(150, 100, 50, 50), "cooldown": 35},
            {"tipo": "atirador", "rect": pygame.Rect(600, 100, 50, 50), "cooldown": 35},
            {"tipo": "perseguidor", "rect": pygame.Rect(250, 320, 50, 50), "dx": 0, "dy": 0, "tempo_mov": 0},
            {"tipo": "perseguidor", "rect": pygame.Rect(500, 320, 50, 50), "dx": 0, "dy": 0, "tempo_mov": 0},
            {"tipo": "perseguidor", "rect": pygame.Rect(350, 450, 50, 50), "dx": 0, "dy": 0, "tempo_mov": 0}
        ]
    
    inimigos_validos = []
    paredes_atuais = criar_paredes_fase(fase) + criar_obstaculos(fase)
    for ini in candidatos:
        colidiu = False
        for p in paredes_atuais:
            if ini["rect"].colliderect(p):
                colidiu = True
                break
        if not colidiu:
            inimigos_validos.append(ini)
    return inimigos_validos

def criar_refens():
    return [
        {"id": 1, "rect": pygame.Rect(100, 180, 50, 50)}, 
        {"id": 2, "rect": pygame.Rect(650, 250, 50, 50)}  
    ]

paredes_convés = criar_paredes_fase(fase_atual)
inimigos = criar_inimigos(fase_atual)
refens_no_mapa = criar_refens()
obstaculos = criar_obstaculos(fase_atual)
todas_as_paredes = paredes_convés + obstaculos

estado_jogo = "MENU_INICIAL"

def resetar_mortes_da_fase():
    for pid in equipe_selecionada:
        p = personagens[pid]
        p["mortes"] = 0
        p["perdido_definitivo"] = False
        p["vivo"] = True

def lidar_com_morte_lider():
    global indice_atual, estado_jogo, membros_caidos, vidas_gerais
    if som_dano is not None:
        som_dano.play()
    
    heroi_atual = personagens[indice_atual]
    heroi_atual["vivo"] = False
    heroi_atual["mortes"] += 1
    
    if heroi_atual["mortes"] >= 2:
        heroi_atual["perdido_definitivo"] = True
        if heroi_atual["id"] in equipe_selecionada:
            equipe_selecionada.remove(heroi_atual["id"])
    else:
        membros_caidos.append({
            "id": heroi_atual["id"],
            "rect": pygame.Rect(jogador_x, jogador_y, 50, 50)
        })

    vivos_na_equipe = [pid for pid in equipe_selecionada if personagens[pid]["vivo"] and not personagens[pid]["perdido_definitivo"]]
    
    if len(vivos_na_equipe) > 0:
        indice_atual = vivos_na_equipe[0]
        estado_jogo = "AGUARDANDO_RESTART_MEMBRO"
    else:
        vidas_gerais -= 1
        membros_caidos.clear() 
        if vidas_gerais > 0 and len(equipe_selecionada) > 0:
            for pid in equipe_selecionada:
                personagens[pid]["vivo"] = True
                personagens[pid]["mortes"] = 0
            indice_atual = equipe_selecionada[0]
            estado_jogo = "AGUARDANDO_RESTART_MEMBRO"
        else:
            estado_jogo = "GAMEOVER"

def desenhar_personagem(x, y, personagem_id, direcao):
    dx, dy = direcao
    if personagem_id == 0 and img_capitao is not None:
        sombra_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_surf, (0, 0, 0, 70), (0, 0, 40, 40))
        tela.blit(sombra_surf, (x + 5, y + 8))
        tela.blit(img_capitao, (x + 3, y + 3))
    elif personagem_id == 1 and img_marujo is not None:
        sombra_surf = pygame.Surface((52, 52), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_surf, (0, 0, 0, 70), (0, 0, 52, 52))
        tela.blit(sombra_surf, (x - 1, y + 2))
        tela.blit(img_marujo, (x - 7, y - 7))
    elif personagem_id == 2 and img_maruja is not None:
        sombra_surf = pygame.Surface((44, 44), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_surf, (0, 0, 0, 70), (0, 0, 44, 44))
        tela.blit(sombra_surf, (x + 3, y + 6))
        tela.blit(img_maruja, (x, y))
    else:
        p_info = personagens[personagem_id]
        pygame.draw.rect(tela, p_info["cor"], (x + 6, y + 6, 38, 38), border_radius=6)
        pygame.draw.rect(tela, PRETO, (x + 6, y + 6, 38, 38), 2, border_radius=6)

    olho_x = x + 25 + (dx * 14)
    olho_y = y + 25 + (dy * 14)
    pygame.draw.circle(tela, BRANCO, (olho_x, olho_y), 3)
    pygame.draw.circle(tela, PRETO, (olho_x, olho_y), 1)

# Loop Principal
rodando = True
while rodando:
    
    # --- MENU PRINCIPAL INTERATIVO ---
    if estado_jogo == "MENU_INICIAL":
        tela.fill(PRETO)
        for i in range(0, LARGURA, 40):
            pygame.draw.line(tela, CINZA_ESCURO, (i, 0), (i, ALTURA), 1)

        titulo = fonte_grande.render("MUTINY TACTICS", True, AMARELO_OURO)
        subtitulo = fonte.render("Uma aventura tática nos sete mares", True, BRANCO)
        
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 120))
        tela.blit(subtitulo, (LARGURA // 2 - subtitulo.get_width() // 2, 180))

        for i, opcao in enumerate(opcoes_lista):
            cor = AMARELO_OURO if i == opcao_menu else BRANCO
            prefixo = "> " if i == opcao_menu else "  "
            texto_opcao = fonte_grande.render(prefixo + opcao, True, cor)
            tela.blit(texto_opcao, (LARGURA // 2 - 120, 280 + (i * 70)))

        instrucao = fonte.render("Use as SETAS para navegar e ENTER para selecionar", True, CINZA_CLARO)
        tela.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, 540))

        marca_dagua = fonte_pequena.render("SyncedCorp.", True, CINZA_SUTIL)
        tela.blit(marca_dagua, (LARGURA - marca_dagua.get_width() - 15, ALTURA - 25))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcao_menu = (opcao_menu - 1) % len(opcoes_lista)
                elif evento.key == pygame.K_DOWN:
                    opcao_menu = (opcao_menu + 1) % len(opcoes_lista)
                elif evento.key == pygame.K_RETURN:
                    if opcao_menu == 0: # JOGAR
                        equipe_liberada = [0]
                        equipe_selecionada = [0]
                        vidas_gerais = 3
                        indice_atual = 0
                        fase_atual = 1
                        tocar_musica_fase(fase_atual)
                        estado_jogo = "JOGANDO"
                    elif opcao_menu == 1: # COMO JOGAR
                        estado_jogo = "TELA_INSTRUCOES"
                    elif opcao_menu == 2: # OPÇÕES
                        estado_jogo = "TELA_OPCOES"
                        estado_origem_opcoes = "MENU_INICIAL"
                        opcao_config_menu = 0
                    elif opcao_menu == 3: # SAIR
                        rodando = False

        pygame.display.flip()
        relogio.tick(FPS)
        continue

    # --- TELA DE OPÇÕES ---
    if estado_jogo == "TELA_OPCOES":
        tela.fill(PRETO)
        
        titulo_op = fonte_grande.render("OPÇÕES", True, AMARELO_OURO)
        tela.blit(titulo_op, (LARGURA // 2 - titulo_op.get_width() // 2, 80))
        
        texto_fs = "TELA CHEIA: LIGADA" if is_fullscreen else "TELA CHEIA: DESLIGADA"
        itens_opcoes = [texto_fs, "VOLTAR"]
        
        for i, opcao in enumerate(itens_opcoes):
            cor = AMARELO_OURO if i == opcao_config_menu else BRANCO
            prefixo = "> " if i == opcao_config_menu else "  "
            texto_opcao = fonte_grande.render(prefixo + opcao, True, cor)
            pos_x = (LARGURA // 2) - (texto_opcao.get_width() // 2)
            tela.blit(texto_opcao, (pos_x, 250 + (i * 70)))
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    opcao_config_menu = (opcao_config_menu - 1) % len(itens_opcoes)
                elif evento.key == pygame.K_DOWN:
                    opcao_config_menu = (opcao_config_menu + 1) % len(itens_opcoes)
                elif evento.key == pygame.K_RETURN:
                    if opcao_config_menu == 0:
                        is_fullscreen = not is_fullscreen
                        flags = pygame.SCALED | (pygame.FULLSCREEN if is_fullscreen else pygame.RESIZABLE)
                        tela = pygame.display.set_mode((LARGURA, ALTURA), flags)
                    elif opcao_config_menu == 1:
                        estado_jogo = estado_origem_opcoes
                elif evento.key == pygame.K_ESCAPE:
                        estado_jogo = estado_origem_opcoes
                        
        pygame.display.flip()
        relogio.tick(FPS)
        continue

    # --- TELA DE INSTRUÇÕES ---
    if estado_jogo == "TELA_INSTRUCOES":
        tela.fill(PRETO)
        
        titulo_inst = fonte_grande.render("COMO JOGAR", True, AMARELO_OURO)
        t1 = fonte.render("- Use as SETAS do teclado para mover o herói.", True, BRANCO)
        t2 = fonte.render("- Pressione [ Z ] para ataque à distância.", True, BRANCO)
        t3 = fonte.render("- Pressione [ X ] para ataque corpo a corpo (Espada).", True, BRANCO)
        t4 = fonte.render("- Resgate reféns e membros caídos para fortalecer o esquadrão.", True, BRANCO)
        t5 = fonte.render("- Alcance a área verde de saída para avançar de fase.", True, BRANCO)
        voltar = fonte.render("Aperte [ ESC ] para voltar ao menu", True, CINZA_CLARO)

        tela.blit(titulo_inst, (LARGURA // 2 - titulo_inst.get_width() // 2, 80))
        tela.blit(t1, (100, 200))
        tela.blit(t2, (100, 250))
        tela.blit(t3, (100, 300))
        tela.blit(t4, (100, 350))
        tela.blit(t5, (100, 400))
        tela.blit(voltar, (LARGURA // 2 - voltar.get_width() // 2, 500))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado_jogo = "MENU_INICIAL"

        pygame.display.flip()
        relogio.tick(FPS)
        continue

    if estado_jogo == "SELECAO_ESQUADRAO":
        tela.fill(PRETO)
        titulo_sel = fonte_grande.render("ESCOLHA SEU ESQUADRÃO (Até 3)", True, AMARELO_OURO)
        instrucao_sel = fonte.render("Pressione o número do herói para alternar (Enter para confirmar)", True, BRANCO)
        tela.blit(titulo_sel, (LARGURA // 2 - titulo_sel.get_width() // 2, 100))
        tela.blit(instrucao_sel, (LARGURA // 2 - instrucao_sel.get_width() // 2, 170))

        y_pos = 250
        for p in personagens:
            if p["id"] in equipe_liberada and not p["perdido_definitivo"]:
                selecionado = p["id"] in equipe_selecionada
                status_txt = "[ X ] SELECIONADO" if selecionado else "[   ] Disponível"
                cor_txt = VERDE_SAIDA if selecionado else BRANCO
                texto_pers = fonte.render(f"[{p['id'] + 1}] {p['nome']} - {status_txt}", True, cor_txt)
                tela.blit(texto_pers, (150, y_pos))
                y_pos += 60

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.KEYDOWN:
                id_escolhido = -1
                if evento.key == pygame.K_1: id_escolhido = 0
                elif evento.key == pygame.K_2: id_escolhido = 1
                elif evento.key == pygame.K_3: id_escolhido = 2

                if id_escolhido != -1 and id_escolhido in equipe_liberada and not personagens[id_escolhido]["perdido_definitivo"]:
                    if id_escolhido in equipe_selecionada:
                        if len(equipe_selecionada) > 1:
                            equipe_selecionada.remove(id_escolhido)
                    else:
                        if len(equipe_selecionada) < 3:
                            equipe_selecionada.append(id_escolhido)

                if evento.key == pygame.K_RETURN and len(equipe_selecionada) > 0:
                    indice_atual = equipe_selecionada[0]
                    resetar_mortes_da_fase()
                    paredes_convés = criar_paredes_fase(fase_atual)
                    inimigos = criar_inimigos(fase_atual)
                    refens_no_mapa = criar_refens()
                    obstaculos = criar_obstaculos(fase_atual)
                    todas_as_paredes = paredes_convés + obstaculos
                    membros_caidos.clear()
                    historico_posicoes.clear()
                    tiros_jogador.clear()
                    tiros_inimigos.clear()
                    golpes_espada.clear()
                    jogador_x, jogador_y = LARGURA // 2, ALTURA - 80
                    bonus_limpeza_concluido = False
                    tocar_musica_fase(fase_atual)
                    estado_jogo = "JOGANDO"

        pygame.display.flip(); relogio.tick(FPS); continue

    if estado_jogo == "AGUARDANDO_RESTART_MEMBRO":
        fundo_cor = MADEIRA_NAVIO if fase_atual == 1 else (AREIA_ILHA if fase_atual == 2 else CAVERNA_FUNDO)
        tela.fill(fundo_cor)
        
        aviso_morte = fonte_grande.render("LÍDER CAÍDO!", True, VERMELHO_BANDANA)
        aviso_continuar = fonte.render(f"Assumindo controle de: {personagens[indice_atual]['nome']}", True, AMARELO_OURO)
        aviso_tecla = fonte.render("Aperte qualquer tecla para continuar", True, BRANCO)
        
        tela.blit(aviso_morte, (LARGURA // 2 - aviso_morte.get_width() // 2, 200))
        tela.blit(aviso_continuar, (LARGURA // 2 - aviso_continuar.get_width() // 2, 270))
        tela.blit(aviso_tecla, (LARGURA // 2 - aviso_tecla.get_width() // 2, 340))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.KEYDOWN:
                historico_posicoes.clear()
                jogador_x, jogador_y = LARGURA // 2, ALTURA - 80
                estado_jogo = "JOGANDO"
        pygame.display.flip(); relogio.tick(FPS); continue

    # ==========================================
    # ESTADO JOGANDO E PAUSADO (LÓGICA)
    # ==========================================
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: rodando = False
            
        if evento.type == pygame.KEYDOWN:
            if estado_jogo == "JOGANDO":
                heroi_atual = personagens[indice_atual]
                
                if evento.key == pygame.K_1 and 0 in equipe_selecionada and personagens[0]["vivo"] and not personagens[0]["perdido_definitivo"]: indice_atual = 0
                if evento.key == pygame.K_2 and 1 in equipe_selecionada and personagens[1]["vivo"] and not personagens[1]["perdido_definitivo"]: indice_atual = 1
                if evento.key == pygame.K_3 and 2 in equipe_selecionada and personagens[2]["vivo"] and not personagens[2]["perdido_definitivo"]: indice_atual = 2
                
                if evento.key == pygame.K_z and heroi_atual["tem_longe"] and cooldown_atual_longe == 0:
                    vel_tiro = 10
                    if heroi_atual["id"] == 2: 
                        direcoes_8 = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
                        for d_x, d_y in direcoes_8:
                            tiros_jogador.append([jogador_x + 25, jogador_y + 25, d_x * vel_tiro, d_y * vel_tiro, 10])
                    else: 
                        dx, dy = direcao_olhar
                        tiros_jogador.append([jogador_x + 25, jogador_y + 25, dx * vel_tiro, dy * vel_tiro, 10])
                    cooldown_atual_longe = heroi_atual["cooldown_longe"]
                    
                if evento.key == pygame.K_x and heroi_atual["tem_perto"] and cooldown_atual_perto == 0:
                    dx, dy = direcao_olhar
                    alcance_espada = 100 if heroi_atual["id"] == 1 else 50
                    tamanho_caixa = 50
                    caixa_dano = pygame.Rect(jogador_x + (dx * alcance_espada), jogador_y + (dy * alcance_espada), tamanho_caixa, tamanho_caixa)
                    golpes_espada.append({"rect": caixa_dano, "tempo": 10}) 
                    cooldown_atual_perto = heroi_atual["cooldown_perto"]
                    
                if evento.key == pygame.K_ESCAPE:
                    estado_jogo = "PAUSADO"
                    opcao_pause = 0
                    
            elif estado_jogo == "PAUSADO":
                if evento.key == pygame.K_UP:
                    opcao_pause = (opcao_pause - 1) % len(opcoes_pause)
                elif evento.key == pygame.K_DOWN:
                    opcao_pause = (opcao_pause + 1) % len(opcoes_pause)
                elif evento.key == pygame.K_RETURN:
                    if opcao_pause == 0: # CONTINUAR
                        estado_jogo = "JOGANDO"
                    elif opcao_pause == 1: # OPÇÕES
                        estado_jogo = "TELA_OPCOES"
                        estado_origem_opcoes = "PAUSADO"
                        opcao_config_menu = 0
                    elif opcao_pause == 2: # MENU PRINCIPAL
                        pygame.mixer.music.stop()
                        estado_jogo = "MENU_INICIAL"
                elif evento.key == pygame.K_ESCAPE:
                    estado_jogo = "JOGANDO"

    if estado_jogo == "JOGANDO":
        heroi_atual = personagens[indice_atual]
        if cooldown_atual_longe > 0: cooldown_atual_longe -= 1
        if cooldown_atual_perto > 0: cooldown_atual_perto -= 1

        if not bonus_limpeza_concluido and len(inimigos) == 0 and len(refens_no_mapa) == 0:
            pontos += 1000
            bonus_limpeza_concluido = True

        teclas = pygame.key.get_pressed()
        vel_base = heroi_atual["vel"]
        jogador_rect_temp = pygame.Rect(jogador_x, jogador_y, tamanho_jogador, tamanho_jogador)
        vel = vel_base * 0.5 if (fase_atual == 2 and jogador_rect_temp.colliderect(zona_agua_praia)) else vel_base
        
        pos_anterior_x, pos_anterior_y = jogador_x, jogador_y
        dx_mov, dy_mov = 0, 0
        
        if teclas[pygame.K_LEFT]: dx_mov = -vel; direcao_olhar = (-1, 0)
        elif teclas[pygame.K_RIGHT]: dx_mov = vel; direcao_olhar = (1, 0)
        if teclas[pygame.K_UP]: dy_mov = -vel; direcao_olhar = (0, -1)
        elif teclas[pygame.K_DOWN]: dy_mov = vel; direcao_olhar = (0, 1)

        dx_mov = round(dx_mov)
        dy_mov = round(dy_mov)

        teste_x = pygame.Rect(jogador_x + dx_mov, jogador_y, tamanho_jogador, tamanho_jogador)
        if not any(teste_x.colliderect(parede) for parede in todas_as_paredes): jogador_x += dx_mov
        
        teste_y = pygame.Rect(jogador_x, jogador_y + dy_mov, tamanho_jogador, tamanho_jogador)
        if not any(teste_y.colliderect(parede) for parede in todas_as_paredes): jogador_y += dy_mov

        if jogador_x != pos_anterior_x or jogador_y != pos_anterior_y:
            historico_posicoes.insert(0, (jogador_x, jogador_y))
            if len(historico_posicoes) > 150: historico_posicoes.pop()

        jogador_rect = pygame.Rect(jogador_x, jogador_y, tamanho_jogador, tamanho_jogador)
        
        if jogador_rect.colliderect(zona_saida):
            if fase_atual < 3:
                fase_atual += 1
                estado_jogo = "SELECAO_ESQUADRAO" 
            else:
                pygame.mixer.music.stop()
                estado_jogo = "VITORIA"

        for refem in refens_no_mapa[:]:
            if jogador_rect.colliderect(refem["rect"]):
                rid = refem["id"]
                if rid not in equipe_liberada: equipe_liberada.append(rid)
                personagens[rid]["vivo"] = True 
                if fase_atual == 1:
                    if rid not in equipe_selecionada: equipe_selecionada.append(rid)
                else:
                    if len(equipe_selecionada) < 3 and rid not in equipe_selecionada: equipe_selecionada.append(rid)
                refens_no_mapa.remove(refem)
                pontos += 500

        for caido in membros_caidos[:]:
            if jogador_rect.colliderect(caido["rect"]):
                membro = personagens[caido["id"]]
                membro["vivo"] = True
                if fase_atual > 1 and len(equipe_selecionada) < 3 and caido["id"] not in equipe_selecionada:
                    equipe_selecionada.append(caido["id"])
                membros_caidos.remove(caido)
                pontos += 300

        for ini in inimigos[:]:
            centro_x_ini = ini["rect"].x + 25; centro_y_ini = ini["rect"].y + 25
            centro_x_jog = jogador_x + 25; centro_y_jog = jogador_y + 25
            dist_x = centro_x_jog - centro_x_ini; dist_y = centro_y_jog - centro_y_ini
            distancia = math.hypot(dist_x, dist_y)

            if ini["tipo"] == "atirador":
                if ini["cooldown"] > 0: ini["cooldown"] -= 1
                elif distancia > 0:
                    vel_tiro_ini = 5 if fase_atual == 1 else (7 if fase_atual == 2 else 8)
                    tiros_inimigos.append([centro_x_ini, centro_y_ini, (dist_x/distancia)*vel_tiro_ini, (dist_y/distancia)*vel_tiro_ini, 10])
                    ini["cooldown"] = 80 if fase_atual == 3 else (100 if fase_atual == 2 else 120)
            elif ini["tipo"] == "perseguidor":
                vetor_costas = (direcao_olhar[0] * -dist_x) + (direcao_olhar[1] * -dist_y)
                ini_dx_mov, ini_dy_mov = 0, 0
                if distancia < 250 and vetor_costas < 0 and distancia > 0:
                    ini_dx_mov = (dist_x / distancia) * 4.0
                    ini_dy_mov = (dist_y / distancia) * 4.0
                else:
                    if ini["tempo_mov"] <= 0:
                        ini["dx"] = random.choice([-2, 0, 2]); ini["dy"] = random.choice([-2, 0, 2])
                        ini["tempo_mov"] = random.randint(30, 90)
                    else:
                        ini_dx_mov = ini["dx"]; ini_dy_mov = ini["dy"]
                        ini["tempo_mov"] -= 1
                
                teste_ini_x = pygame.Rect(ini["rect"].x + ini_dx_mov, ini["rect"].y, 50, 50)
                if not any(teste_ini_x.colliderect(p) for p in todas_as_paredes) and not teste_ini_x.colliderect(safe_zone):
                    ini["rect"].x += ini_dx_mov
                else: ini["dx"] *= -1 
                    
                teste_ini_y = pygame.Rect(ini["rect"].x, ini["rect"].y + ini_dy_mov, 50, 50)
                if not any(teste_ini_y.colliderect(p) for p in todas_as_paredes) and not teste_ini_y.colliderect(safe_zone):
                    ini["rect"].y += ini_dy_mov
                else: ini["dy"] *= -1 

            if jogador_rect.colliderect(ini["rect"]):
                lidar_com_morte_lider()
                break

        for t in tiros_jogador[:]:
            t[0] += t[2]; t[1] += t[3]
            tiro_rect = pygame.Rect(t[0], t[1], t[4], t[4])
            if any(tiro_rect.colliderect(p) for p in todas_as_paredes) or t[0] < 0 or t[0] > LARGURA or t[1] < 0 or t[1] > ALTURA:
                tiros_jogador.remove(t); continue
            for ini in inimigos[:]:
                if tiro_rect.colliderect(ini["rect"]):
                    inimigos.remove(ini); pontos += 100
                    if som_dano is not None: som_dano.play()
                    if t in tiros_jogador: tiros_jogador.remove(t)
                    break

        for t in tiros_inimigos[:]:
            t[0] += t[2]; t[1] += t[3]
            tiro_rect = pygame.Rect(t[0], t[1], t[4], t[4])
            if tiro_rect.colliderect(safe_zone) or any(tiro_rect.colliderect(p) for p in todas_as_paredes) or t[0] < 0 or t[0] > LARGURA or t[1] < 0 or t[1] > ALTURA:
                tiros_inimigos.remove(t); continue
            if tiro_rect.colliderect(jogador_rect):
                tiros_inimigos.remove(t)
                lidar_com_morte_lider()
                break

        for golpe in golpes_espada[:]:
            golpe["tempo"] -= 1
            if golpe["tempo"] <= 0: golpes_espada.remove(golpe); continue
            for ini in inimigos[:]:
                if golpe["rect"].colliderect(ini["rect"]):
                    inimigos.remove(ini); pontos += 100
                    if som_dano is not None: som_dano.play()

    # ==========================================
    # RENDERIZAÇÃO 
    # ==========================================
    if estado_jogo in ["JOGANDO", "PAUSADO"]:
        heroi_atual = personagens[indice_atual]
        if fase_atual == 1:
            tela.fill(MADEIRA_NAVIO)
            for y_t in range(0, ALTURA, 40):
                pygame.draw.line(tela, MADEIRA_ESCURA, (0, y_t), (LARGURA, y_t), 2)
            pygame.draw.arc(tela, COR_CORDA, (350, 480, 40, 30), 0, 3.14, 3)
            pygame.draw.arc(tela, COR_CORDA, (370, 490, 40, 30), 0, 3.14, 3)
        elif fase_atual == 2:
            tela.fill(AREIA_ILHA)
            for i in range(40):
                px = (i * 137) % LARGURA
                py = (i * 83) % ALTURA
                pygame.draw.circle(tela, AREIA_ESCURA, (px, py), 2)
            pygame.draw.rect(tela, AGUA_BORDA, zona_agua_praia, border_radius=15)
            pygame.draw.rect(tela, AGUA_LAGOA, zona_agua_praia.inflate(-8, -8), border_radius=12)
            pygame.draw.arc(tela, BRANCO, (zona_agua_praia.x + 30, zona_agua_praia.y + 40, 40, 20), 0, 3.14, 2)
            pygame.draw.arc(tela, BRANCO, (zona_agua_praia.x + 90, zona_agua_praia.y + 70, 40, 20), 0, 3.14, 2)
        else:
            tela.fill(CAVERNA_FUNDO)
            for i in range(30):
                rx = (i * 211) % LARGURA
                ry = (i * 97) % ALTURA
                pygame.draw.rect(tela, CAVERNA_DETALHE, (rx, ry, 12, 6))
        
        cor_safe = MADEIRA_SAFE if fase_atual == 1 else (PEDRA_ILHA if fase_atual == 2 else CINZA_ESCURO)
        pygame.draw.rect(tela, cor_safe, safe_zone, border_radius=8)
        pygame.draw.rect(tela, AMARELO_OURO, safe_zone, 2, border_radius=8)
        
        zona_saida = pygame.Rect(300, 0, 200, 40)
        pygame.draw.rect(tela, VERDE_SAIDA, zona_saida, border_radius=4)
        texto_saida = fonte.render(f"SAÍDA (Fase {fase_atual})", True, PRETO)
        tela.blit(texto_saida, (zona_saida.x + (zona_saida.width - texto_saida.get_width()) // 2, 8))

        for parede in paredes_convés:
            cor_p = MADEIRA_CLARA if fase_atual == 1 else (PEDRA_ILHA if fase_atual == 2 else CINZA_ESCURO)
            pygame.draw.rect(tela, cor_p, parede, border_radius=4)
            pygame.draw.rect(tela, PRETO, parede, 2, border_radius=4)

        for obs in obstaculos:
            if fase_atual == 1:
                if img_barril is not None: tela.blit(img_barril, (obs.x, obs.y))
                else:
                    pygame.draw.circle(tela, COR_BARRIL, (obs.x + 35, obs.y + 35), 32)
                    pygame.draw.circle(tela, PRETO, (obs.x + 35, obs.y + 35), 32, 2)
            elif fase_atual == 2:
                if img_coqueiro is not None: tela.blit(img_coqueiro, (obs.x, obs.y))
                else:
                    pygame.draw.rect(tela, (110, 70, 40), (obs.x + 28, obs.y + 20, 14, 50))
                    pygame.draw.circle(tela, (30, 140, 40), (obs.x + 35, obs.y + 25), 26)
            else:
                if img_cristal is not None: tela.blit(img_cristal, (obs.x, obs.y))
                else:
                    pygame.draw.circle(tela, ROCHA_CAVERNA, (obs.x + 35, obs.y + 35), 32)
                    pygame.draw.circle(tela, (100, 220, 240), (obs.x + 28, obs.y + 28), 10)

        for caido in membros_caidos:
            membro_info = personagens[caido["id"]]
            pygame.draw.rect(tela, membro_info["cor"], caido["rect"], border_radius=10)
            texto_caido = fonte.render("CAÍDO", True, VERMELHO_BANDANA)
            tela.blit(texto_caido, (caido["rect"].x - 10, caido["rect"].y - 28))

        for refem in refens_no_mapa:
            membro_id = refem["id"]
            membro_info = personagens[membro_id]
            if membro_id == 1 and img_marujo is not None:
                tela.blit(pygame.transform.scale(img_marujo, (38, 38)), (refem["rect"].x + 6, refem["rect"].y + 6))
            elif membro_id == 2 and img_maruja is not None:
                tela.blit(pygame.transform.scale(img_maruja, (38, 38)), (refem["rect"].x + 6, refem["rect"].y + 6))
            else:
                pygame.draw.rect(tela, membro_info["cor"], refem["rect"], border_radius=6)
            pygame.draw.rect(tela, AMARELO_OURO, refem["rect"], 3, border_radius=8)
            texto_socorro = fonte.render("SOS", True, AMARELO_OURO)
            tela.blit(texto_socorro, (refem["rect"].x + 5, refem["rect"].y - 28))

        for ini in inimigos:
            sombra_ini = pygame.Surface((44, 44), pygame.SRCALPHA)
            pygame.draw.ellipse(sombra_ini, (0, 0, 0, 70), (2, 2, 40, 40))
            tela.blit(sombra_ini, (ini["rect"].x + 3, ini["rect"].y + 6))
            if ini["tipo"] == "atirador" and img_atirador is not None:
                tela.blit(img_atirador, (ini["rect"].x, ini["rect"].y))
                pygame.draw.rect(tela, PRETO, ini["rect"], 2, border_radius=6)
            elif ini["tipo"] == "perseguidor" and img_perseguidor is not None:
                tela.blit(img_perseguidor, (ini["rect"].x, ini["rect"].y))
                pygame.draw.rect(tela, PRETO, ini["rect"], 2, border_radius=6)
            else:
                cor_fallback = LARANJA_FOGO if ini["tipo"] == "atirador" else ROXO_MAGIA
                pygame.draw.rect(tela, cor_fallback, ini["rect"], border_radius=8)
                pygame.draw.rect(tela, PRETO, ini["rect"], 2, border_radius=8)
                
        for t in tiros_jogador: pygame.draw.circle(tela, AMARELO_OURO, (int(t[0]), int(t[1])), 6)
        for t in tiros_inimigos: pygame.draw.circle(tela, VERMELHO_BANDANA, (int(t[0]), int(t[1])), 6)
        
        for golpe in golpes_espada: 
            pygame.draw.rect(tela, BRANCO, golpe["rect"], border_radius=4)
            pygame.draw.rect(tela, AMARELO_OURO, golpe["rect"], 2, border_radius=4)
            
        distancia_fila = 15
        ordem_desenho = 1
        for id_membro in equipe_selecionada:
            if id_membro != indice_atual and personagens[id_membro]["vivo"] and not personagens[id_membro]["perdido_definitivo"]:
                idx_historico = ordem_desenho * distancia_fila
                pos_x, pos_y = historico_posicoes[idx_historico] if idx_historico < len(historico_posicoes) else (jogador_x, jogador_y)
                desenhar_personagem(pos_x, pos_y, id_membro, direcao_olhar)
                ordem_desenho += 1

        desenhar_personagem(jogador_x, jogador_y, indice_atual, direcao_olhar)

        # HUD
        pygame.draw.rect(tela, CINZA_ESCURO, (0, ALTURA - 45, LARGURA, 45))
        pygame.draw.line(tela, AMARELO_OURO, (0, ALTURA - 45), (LARGURA, ALTURA - 45), 3)
        texto_hud = fonte.render(f"FASE: {fase_atual}/3   |   VIDAS DA EQUIPE: {vidas_gerais}   |   PONTOS: {pontos}   |   LÍDER: {heroi_atual['nome']}", True, BRANCO)
        tela.blit(texto_hud, (15, ALTURA - 35))

    if estado_jogo == "VITORIA":
        tela.fill(PRETO)
        texto_vitoria = fonte_grande.render("CAMPANHA CONCLUÍDA!", True, VERDE_SAIDA)
        texto_pontos = fonte_grande.render(f"PONTOS: {pontos}", True, AMARELO_OURO)
        tela.blit(texto_vitoria, (LARGURA // 2 - texto_vitoria.get_width() // 2, ALTURA // 2 - 60))
        tela.blit(texto_pontos, (LARGURA // 2 - texto_pontos.get_width() // 2, ALTURA // 2 + 10))
        
    elif estado_jogo == "GAMEOVER":
        tela.fill(PRETO)
        texto_derrota = fonte_grande.render("GAME OVER! Equipe dizimada.", True, VERMELHO_BANDANA)
        sub_derrota = fonte.render("Aperte 'R' para reiniciar a campanha", True, BRANCO)
        tela.blit(texto_derrota, (LARGURA // 2 - texto_derrota.get_width() // 2, ALTURA // 2 - 40))
        tela.blit(sub_derrota, (LARGURA // 2 - sub_derrota.get_width() // 2, ALTURA // 2 + 20))
        
        if pygame.key.get_pressed()[pygame.K_r]:
            fase_atual = 1
            personagens = criar_personagens_base()
            paredes_convés = criar_paredes_fase(fase_atual)
            inimigos = criar_inimigos(fase_atual)
            refens_no_mapa = criar_refens()
            obstaculos = criar_obstaculos(fase_atual)
            todas_as_paredes = paredes_convés + obstaculos
            equipe_liberada = [0]
            equipe_selecionada = [0]
            vidas_gerais = 3
            membros_caidos.clear()
            historico_posicoes.clear()
            tiros_jogador.clear()
            tiros_inimigos.clear()
            golpes_espada.clear()
            jogador_x, jogador_y = LARGURA // 2, ALTURA - 80
            indice_atual = 0
            pontos = 0
            bonus_limpeza_concluido = False
            pygame.mixer.music.stop()
            estado_jogo = "JOGANDO"

    # Desenho do Menu de Pausa Lateral
    if estado_jogo == "PAUSADO":
        sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 160))
        tela.blit(sombra, (0, 0))

        largura_painel = 280
        rect_painel = pygame.Rect(LARGURA - largura_painel, 0, largura_painel, ALTURA)
        pygame.draw.rect(tela, CINZA_ESCURO, rect_painel)
        pygame.draw.rect(tela, AMARELO_OURO, rect_painel, 3)

        titulo_pause = fonte_grande.render("PAUSA", True, AMARELO_OURO)
        tela.blit(titulo_pause, (LARGURA - largura_painel + (largura_painel // 2 - titulo_pause.get_width() // 2), 60))

        for i, opcao in enumerate(opcoes_pause):
            cor = AMARELO_OURO if i == opcao_pause else BRANCO
            prefixo = "> " if i == opcao_pause else "  "
            texto_opcao = fonte.render(prefixo + opcao, True, cor)
            tela.blit(texto_opcao, (LARGURA - largura_painel + 30, 200 + (i * 60)))

        marca_pause = fonte_pequena.render("SyncedCorp.", True, CINZA_SUTIL)
        tela.blit(marca_pause, (LARGURA - largura_painel + (largura_painel // 2 - marca_pause.get_width() // 2), ALTURA - 40))

    pygame.display.flip()
    relogio.tick(FPS)

pygame.quit()
sys.exit()