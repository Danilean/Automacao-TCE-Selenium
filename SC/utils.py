import os

def limpar_pasta(pasta):
    for arquivo in os.listdir(pasta):
        file_path = os.path.join(pasta, arquivo)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
        except Exception as e:
            print(f"Erro ao remover {file_path}: {e}")
