import wave
import struct
import random

# Configurações do áudio
taxa_amostragem = 44100
duracao = 0.3 # 0.3 segundos

# Cria o arquivo dano.wav
print("Gerando som de dano retro...")
with wave.open('dano.wav', 'w') as arquivo_wav:
    arquivo_wav.setnchannels(1) # Áudio Mono
    arquivo_wav.setsampwidth(2) # 16-bit
    arquivo_wav.setframerate(taxa_amostragem)
    
    # Gera o som (um ruído áspero de batida que vai diminuindo)
    for i in range(int(taxa_amostragem * duracao)):
        volume = 1 - (i / (taxa_amostragem * duracao)) # Vai abaixando o volume (Fade out)
        valor = int(random.uniform(-30000, 30000) * volume) # Ruído aleatório (estilo explosão)
        dados = struct.pack('<h', valor)
        arquivo_wav.writeframesraw(dados)

print("Sucesso! O arquivo 'dano.wav' foi criado na sua pasta.")