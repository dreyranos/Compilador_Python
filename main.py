import flet as ft
import os
from styles import *
from compiler_engine import CompilerEngine

def main(page: ft.Page):
    page.title = "Python Project Compiler Pro"
    page.bgcolor = BACKGROUND
    page.theme = THEME
    page.padding = 40
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = True

    # State Variables
    selected_script = ft.Ref[ft.TextField]()
    selected_icon = ft.Ref[ft.TextField]()
    add_data_field = ft.Ref[ft.TextField]()
    hidden_imports_field = ft.Ref[ft.TextField]()
    one_file_toggle = ft.Ref[ft.Switch]()
    noconsole_toggle = ft.Ref[ft.Switch]()
    terminal_output = ft.Ref[ft.Column]()
    compile_btn = ft.Ref[ft.ElevatedButton]()
    progress_bar = ft.Ref[ft.ProgressBar]()

    # Handlers
    def on_output(text: str):
        terminal_output.current.controls.append(
            ft.Text(text.strip(), color=TEXT_SECONDARY, size=12, font_family="monospace")
        )
        page.update()

    def on_finished(code: int):
        progress_bar.current.visible = False
        compile_btn.current.disabled = False
        status = "Sucesso!" if code == 0 else f"Falhou com código {code}"
        color = ACCENT if code == 0 else ft.colors.RED_400
        terminal_output.current.controls.append(
            ft.Text(f"\n--- {status} ---", color=color, weight=ft.FontWeight.BOLD)
        )
        page.update()
        page.snack_bar = ft.SnackBar(ft.Text(f"Compilação terminada: {status}"), bgcolor=color)
        page.snack_bar.open = True

    engine = CompilerEngine(on_output, on_finished)

    def start_compile(e):
        if not selected_script.current.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecione o script principal!"), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return

        compile_btn.current.disabled = True
        progress_bar.current.visible = True
        terminal_output.current.controls.clear()
        
        # Build options
        data_list = [d.strip() for d in add_data_field.current.value.split(",") if d.strip()]
        hidden_list = [h.strip() for h in hidden_imports_field.current.value.split(",") if h.strip()]
        
        cmd = engine.build_command(
            script_path=selected_script.current.value,
            one_file=one_file_toggle.current.value,
            noconsole=noconsole_toggle.current.value,
            icon_path=selected_icon.current.value,
            add_data=data_list,
            hidden_imports=hidden_list
        )
        
        engine.run_compilation(cmd)
        page.update()

    # File Pickers Logic (Standard Flet Style)
    def pick_script_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_script.current.value = e.files[0].path
            page.update()

    def pick_icon_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_icon.current.value = e.files[0].path
            page.update()

    def pick_assets_result(e: ft.FilePickerResultEvent):
        if e.files:
            current = add_data_field.current.value or ""
            new_assets = [f"{f.path};." for f in e.files]
            if current:
                add_data_field.current.value = f"{current}, {', '.join(new_assets)}"
            else:
                add_data_field.current.value = ", ".join(new_assets)
            page.update()

    script_picker = ft.FilePicker(on_result=pick_script_result)
    icon_picker = ft.FilePicker(on_result=pick_icon_result)
    asset_picker = ft.FilePicker(on_result=pick_assets_result)
    page.overlay.extend([script_picker, icon_picker, asset_picker])

    # UI Layout
    header = ft.Row(
        [
            ft.Icon(ft.icons.TERMINAL_ROUNDED, color=PRIMARY, size=40),
            ft.Column([
                ft.Text("Python Compiler Pro", size=32, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Text("Transforme seus projetos em executáveis profissionais", color=TEXT_SECONDARY),
            ], spacing=0)
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    config_card = ft.Container(
        content=ft.Column([
            ft.Text("Configurações do Projeto", size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ft.Divider(color=ft.colors.with_opacity(0.1, TEXT_SECONDARY)),
            
            # Script Path
            ft.Row([
                ft.TextField(ref=selected_script, label="Script Principal (.py)", expand=True, **INPUT_STYLE),
                ft.IconButton(ft.icons.FOLDER_OPEN, on_click=lambda _: script_picker.pick_files(allowed_extensions=["py", "pyw"]), icon_color=PRIMARY)
            ]),
            
            # Icon Path
            ft.Row([
                ft.TextField(ref=selected_icon, label="Ícone (.ico)", expand=True, **INPUT_STYLE),
                ft.IconButton(ft.icons.IMAGE, on_click=lambda _: icon_picker.pick_files(allowed_extensions=["ico"]), icon_color=PRIMARY)
            ]),

            # Assets selection
            ft.Row([
                ft.TextField(ref=add_data_field, label="Arquivos Extras (origem;destino)", hint_text="Ex: config.json;.", expand=True, **INPUT_STYLE),
                ft.IconButton(ft.icons.ATTACH_FILE, on_click=lambda _: asset_picker.pick_files(allow_multiple=True), icon_color=PRIMARY)
            ]),
            
            ft.TextField(ref=hidden_imports_field, label="Hidden Imports (Ex: pandas, openpyxl)", helper_text="Pacotes não detectados (separe por vírgula)", **INPUT_STYLE),
            
            ft.Row([
                ft.Switch(ref=one_file_toggle, label="Arquivo Único (.exe)", value=True, active_color=PRIMARY),
                ft.Switch(ref=noconsole_toggle, label="Ocultar Console (Windowed)", value=False, active_color=PRIMARY),
            ], alignment=ft.MainAxisAlignment.START, spacing=30),
            
            ft.VerticalDivider(height=20),
            
            ft.ElevatedButton(
                ref=compile_btn,
                text="COMPILAR PROJETO",
                icon=ft.icons.PLAY_ARROW_ROUNDED,
                style=BUTTON_STYLE,
                height=50,
                on_click=start_compile
            ),
            ft.ProgressBar(ref=progress_bar, visible=False, color=PRIMARY, bgcolor=SURFACE)
        ], spacing=20),
        **CARD_STYLE
    )

    terminal_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Saída do Compilador", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.IconButton(ft.icons.DELETE_SWEEP, on_click=lambda _: terminal_output.current.controls.clear() or page.update(), icon_color=TEXT_SECONDARY)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.ListView(
                    ref=terminal_output,
                    expand=True,
                    spacing=5,
                    auto_scroll=True
                ),
                bgcolor=ft.colors.BLACK,
                padding=15,
                border_radius=8,
                expand=True
            )
        ], expand=True),
        **CARD_STYLE,
        expand=True
    )

    page.add(
        ft.Column([
            header,
            ft.Row([
                ft.Column([config_card], width=450),
                terminal_card
            ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
        ], expand=True)
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8553)
