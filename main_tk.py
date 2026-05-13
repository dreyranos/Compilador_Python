import customtkinter as ctk
import os
import threading
from tkinter import filedialog, messagebox
from compiler_engine import CompilerEngine

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Compilador Pyhton dev Andrey")
        self.geometry("1000x700")

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Left Panel (Config)
        self.left_panel = ctk.CTkFrame(self, corner_radius=10)
        self.left_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.label_title = ctk.CTkLabel(self.left_panel, text="Compilador Pyhton dev Andrey", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=20)

        # Script Selection
        self.script_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.script_frame.pack(fill="x", padx=20, pady=5)
        self.entry_script = ctk.CTkEntry(self.script_frame, placeholder_text="Script Principal (.py)")
        self.entry_script.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_script = ctk.CTkButton(self.script_frame, text="📁", width=40, command=self.pick_script)
        self.btn_script.pack(side="right")

        # Icon Selection
        self.icon_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.icon_frame.pack(fill="x", padx=20, pady=5)
        self.entry_icon = ctk.CTkEntry(self.icon_frame, placeholder_text="Ícone (.ico)")
        self.entry_icon.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_icon = ctk.CTkButton(self.icon_frame, text="🖼️", width=40, command=self.pick_icon)
        self.btn_icon.pack(side="right")

        # Assets Selection
        self.assets_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.assets_frame.pack(fill="x", padx=20, pady=5)
        self.entry_assets = ctk.CTkEntry(self.assets_frame, placeholder_text="Arquivos Extras (origem;destino)")
        self.entry_assets.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_assets = ctk.CTkButton(self.assets_frame, text="📎", width=40, command=self.pick_assets)
        self.btn_assets.pack(side="right")

        # Requirements Selection
        self.req_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.req_frame.pack(fill="x", padx=20, pady=5)
        self.entry_req = ctk.CTkEntry(self.req_frame, placeholder_text="requirements.txt (Opcional)")
        self.entry_req.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.btn_req = ctk.CTkButton(self.req_frame, text="📄", width=40, command=self.pick_req)
        self.btn_req.pack(side="right")

        # Hidden Imports
        self.entry_hidden = ctk.CTkEntry(self.left_panel, placeholder_text="Hidden Imports (pandas, flask...)")
        self.entry_hidden.pack(fill="x", padx=20, pady=10)

        # Options
        self.switch_onefile = ctk.CTkSwitch(self.left_panel, text="Arquivo Único (.exe)")
        self.switch_onefile.select()
        self.switch_onefile.pack(pady=5, padx=20, anchor="w")

        self.switch_noconsole = ctk.CTkSwitch(self.left_panel, text="Ocultar Console (Windowed)")
        self.switch_noconsole.pack(pady=5, padx=20, anchor="w")

        self.switch_clean = ctk.CTkSwitch(self.left_panel, text="Ambiente Isolado (Venv + Auto-Clean)", text_color="#10b981")
        self.switch_clean.pack(pady=5, padx=20, anchor="w")

        # Progress
        self.progress = ctk.CTkProgressBar(self.left_panel)
        self.progress.pack(fill="x", padx=20, pady=20)
        self.progress.set(0)

        # Compile Button
        self.btn_compile = ctk.CTkButton(self.left_panel, text="COMPILAR PROJETO", font=ctk.CTkFont(weight="bold"), 
                                        height=40, command=self.start_compile)
        self.btn_compile.pack(pady=20, padx=20, fill="x")

        # Right Panel (Terminal)
        self.right_panel = ctk.CTkFrame(self, corner_radius=10, fg_color="#000000")
        self.right_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.terminal = ctk.CTkTextbox(self.right_panel, font=("Consolas", 12), text_color="#00FF00")
        self.terminal.pack(fill="both", expand=True, padx=10, pady=10)

        # Engine
        self.engine = CompilerEngine(self.on_output, self.on_finished)

    def on_output(self, text):
        self.terminal.insert("end", text)
        self.terminal.see("end")

    def on_finished(self, code):
        self.progress.set(0)
        self.progress.stop()
        self.btn_compile.configure(state="normal")
        if code == 0:
            messagebox.showinfo("Sucesso", "Compilação concluída com sucesso!")
        else:
            messagebox.showerror("Erro", f"Compilação falhou com código {code}")

    def pick_script(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py *.pyw")])
        if path:
            self.entry_script.delete(0, "end")
            self.entry_script.insert(0, path)

    def pick_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if path:
            self.entry_icon.delete(0, "end")
            self.entry_icon.insert(0, path)

    def pick_req(self):
        path = filedialog.askopenfilename(filetypes=[("Requirements", "*.txt")])
        if path:
            self.entry_req.delete(0, "end")
            self.entry_req.insert(0, path)

    def pick_assets(self):
        paths = filedialog.askopenfilenames()
        if paths:
            current = self.entry_assets.get()
            new_assets = [f"{p};." for p in paths]
            if current:
                self.entry_assets.delete(0, "end")
                self.entry_assets.insert(0, f"{current}, {', '.join(new_assets)}")
            else:
                self.entry_assets.insert(0, ", ".join(new_assets))

    def start_compile(self):
        script = self.entry_script.get()
        if not script:
            messagebox.showwarning("Aviso", "Selecione o script principal!")
            return

        self.btn_compile.configure(state="disabled")
        self.terminal.delete("1.0", "end")
        self.progress.start()

        data_list = [d.strip() for d in self.entry_assets.get().split(",") if d.strip()]
        hidden_list = [h.strip() for h in self.entry_hidden.get().split(",") if h.strip()]
        
        # New: Venv isolation logic
        use_venv = self.switch_clean.get()
        req_file = self.entry_req.get()

        cmd = self.engine.build_command(
            script_path=script,
            one_file=self.switch_onefile.get(),
            noconsole=self.switch_noconsole.get(),
            icon_path=self.entry_icon.get(),
            add_data=data_list,
            hidden_imports=hidden_list
        )

        def compile_thread():
            if use_venv:
                self.on_output(">>> Iniciando Modo Ambiente Isolado...\n")
                # Add logic to create venv and install requirements if needed
                # For simplicity in MVP, the engine can handle this or we can pass it
                pass
            
            self.engine.run_compilation(cmd, use_venv=use_venv, req_path=req_file)

        threading.Thread(target=compile_thread, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
