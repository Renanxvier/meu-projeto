## Mutiny Tactics

Mutiny Tactics é um jogo de ação e aventura com visão top-down. Lidere um grupo de piratas, enfrente inimigos, resgate companheiros e atravesse três fases até concluir a campanha.
Requisitos

    Python 3
    Pygame

Como executar

Na pasta raiz do repositório, instale o Pygame e inicie o jogo:

python -m pip install pygame
python JogoPirata/src/jogo_principal.py

No Windows, se o comando python não estiver disponível, tente usar py no lugar dele.
Como jogar

No menu, use as setas para navegar e Enter para selecionar. A opção Como jogar também mostra os controles dentro do jogo.
Tecla 	Ação
Setas 	Mover o personagem
Z 	Ataque à distância, quando disponível para o personagem
X 	Ataque corpo a corpo, quando disponível para o personagem
1, 2, 3 	Alternar para um integrante selecionado e disponível do esquadrão
Esc 	Abrir ou fechar o menu de pausa
R 	Reiniciar a campanha após o game over

Resgate os reféns para liberar personagens para o esquadrão e encontre a saída verde para avançar. Antes das fases seguintes, você pode escolher até três personagens liberados. As habilidades variam entre integrantes. A campanha termina ao concluir a terceira fase; se a equipe for derrotada, reinicie com R.

No menu Opções, é possível alternar entre janela e tela cheia.
Arquivos do projeto

    src/jogo_principal.py: jogo principal.
    src/jogo.py: outra versão do jogo.
    src/criar_caveira.py, src/criar_rum.py, src/criar_som.py: scripts auxiliares.
    assets/: imagens, efeitos sonoros e músicas usados pelo jogo.

Gerar executável no Windows

Na pasta raiz do repositório, instale o PyInstaller e gere o executável usando a configuração do projeto:

python -m pip install pyinstaller
pyinstaller --clean jogo_principal.spec

O executável será criado em dist/jogo_principal.exe. As pastas build/ e dist/ são artefatos locais de compilação e não fazem parte dos arquivos versionados do projeto.
