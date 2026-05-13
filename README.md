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

## 📦 Gestão de Dependências

1.  **Detecção Automática**: O PyInstaller analisa seus imports e inclui as bibliotecas.
2.  **Modo Ambiente Isolado (Novo! 🚀)**: Você pode ativar esta opção para que o compilador crie um ambiente virtual (`venv`) temporário, instale apenas as dependências necessárias (via `requirements.txt`) e compile o projeto de forma limpa. Ao finalizar, o ambiente é excluído automaticamente, mantendo seu sistema limpo.
3.  **Vínculo com o Ambiente**: Se o modo isolado estiver desativado, ele utiliza as bibliotecas instaladas no seu Python global.
4.  **Hidden Imports**: Para bibliotecas não detectadas automaticamente.
5.  **Arquivos Não-Python**: Recursos extras (imagens, JSON) devem ser incluídos no campo **Arquivos Extras**.

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
