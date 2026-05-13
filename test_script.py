import os
import time

def main():
    print("Iniciando Script de Teste...")
    print(f"Diretório atual: {os.getcwd()}")
    
    # Simular o uso de uma dependência
    try:
        import httpx
        print(f"Httpx instalado! Versão: {httpx.__version__}")
    except ImportError:
        print("Httpx não encontrado.")

    print("Este é um script de teste compilado com sucesso.")
    time.sleep(2)
    print("Fechando em 3 segundos...")
    time.sleep(3)

if __name__ == "__main__":
    main()
