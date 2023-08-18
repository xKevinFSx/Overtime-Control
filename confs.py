# .gitignore
from cryptography.fernet import Fernet

api_key = 'fa43fbe79b23fc7dbb8ad3c17550bf9b47c4ea1b'

def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_arquivo:
        chave_arquivo.write(chave)

def carregar_chave():
    with open("chave.key", "rb") as chave_arquivo:
        return chave_arquivo.read()

#Verificar se a chave já existe, senão gerar e salvar
try:
    carregar_chave()
except FileNotFoundError:
    gerar_chave()
    
    
crip_key = carregar_chave()
cipher_suite = Fernet(crip_key)