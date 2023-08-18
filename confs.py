# .gitignore
from cryptography.fernet import Fernet

api_key = 'fa43fbe79b23fc7dbb8ad3c17550bf9b47c4ea1b'

def gerar_chave():
    chave = Fernet.generate_key()
    chave_db = Fernet.generate_key()
    with open("chave.key", "wb") as chave_arquivo:
        chave_arquivo.write(chave)
    with open("chave_db.key", "wb") as chave_banco:
        chave_banco.write(chave_db)
    
def carregar_chave():
    with open("chave.key", "rb") as chave_arquivo:
        return chave_arquivo.read()
    
def carregar_chave_db(): 
    with open("chave_db.key", "rb") as chave_banco:
        return chave_banco.read()

#Verificar se a chave já existe, senão gerar e salvar
try:
    carregar_chave()
    carregar_chave_db()
except FileNotFoundError:
    gerar_chave()
    

    
db_key = carregar_chave_db()    
crip_key = carregar_chave()
cipher_suite = Fernet(crip_key)