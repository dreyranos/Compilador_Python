# Compilador Pyhton dev Andrey

Este é um compilador de projetos Python com interface gráfica premium desenvolvida em **CustomTkinter**. Ele permite transformar scripts Python (.py) em executáveis (.exe) de forma simples e profissional.

## 🚀 Funcionalidades

- **Interface Nativa Premium**: Design moderno com suporte a Dark Mode.
- **Seleção de Assets**: Suporte para incluir arquivos e pastas extras no executável.
- **Configurações Avançadas**: 
  - One-file (Arquivo único)
  - Windowed/Console mode
  - Suporte a ícones customizados (.ico)
  - Hidden imports
- **Terminal Integrado**: Acompanhe o processo de compilação em tempo real.

## 🛠️ Requisitos

- Python 3.x
- Bibliotecas: `customtkinter`, `pyinstaller`

Instale as dependências com:
```bash
pip install customtkinter pyinstaller
```

## 📖 Como Usar

1. Execute o arquivo `main_tk.py`:
   ```bash
   python main_tk.py
   ```
2. Selecione o script principal do seu projeto.
3. (Opcional) Adicione ícones e arquivos extras.
4. Clique em **COMPILAR PROJETO**.
5. O executável será gerado na pasta `dist/`.

## 📂 Projeto de Teste

O repositório inclui uma pasta `test_project/` para validar o funcionamento de assets e bibliotecas externas (como `requests`) após a compilação.

---
Desenvolvido por Andrey.
