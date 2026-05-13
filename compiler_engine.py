import subprocess
import os
import shlex
import threading
from typing import Callable, List, Optional

class CompilerEngine:
    def __init__(self, on_output: Callable[[str], None], on_finished: Callable[[int], None]):
        self.on_output = on_output
        self.on_finished = on_finished
        self.process: Optional[subprocess.Popen] = None

    def build_command(
        self,
        script_path: str,
        one_file: bool = True,
        noconsole: bool = False,
        icon_path: Optional[str] = None,
        add_data: List[str] = None,
        hidden_imports: List[str] = None,
        output_dir: str = "dist"
    ) -> List[str]:
        cmd = ["python", "-m", "PyInstaller", "--clean", "--noconfirm"]
        
        if one_file:
            cmd.append("--onefile")
        else:
            cmd.append("--onedir")
            
        if noconsole:
            cmd.append("--windowed")
        else:
            cmd.append("--console")
            
        if icon_path and os.path.exists(icon_path):
            cmd.append(f"--icon={icon_path}")
            
        if add_data:
            for item in add_data:
                # Format: source;dest (Windows)
                cmd.append(f"--add-data={item}")
                
        if hidden_imports:
            for imp in hidden_imports:
                cmd.append(f"--hidden-import={imp}")
                
        cmd.append(f"--distpath={output_dir}")
        cmd.append(script_path)
        
        return cmd

    def run_compilation(self, command: List[str], use_venv: bool = False, req_path: str = None):
        temp_dir = None
        try:
            if use_venv:
                import tempfile
                import shutil
                import venv
                
                temp_dir = tempfile.mkdtemp(prefix="py_comp_venv_")
                self.on_output(f">>> Criando ambiente virtual em: {temp_dir}\n")
                venv.create(temp_dir, with_pip=True)
                
                # Path to venv python/pip
                python_exe = os.path.join(temp_dir, "Scripts", "python.exe")
                pip_exe = os.path.join(temp_dir, "Scripts", "pip.exe")
                
                self.on_output(">>> Instalando PyInstaller no ambiente isolado...\n")
                subprocess.run([pip_exe, "install", "pyinstaller"], check=True, capture_output=True)
                
                if req_path and os.path.exists(req_path):
                    self.on_output(f">>> Instalando dependências de: {req_path}\n")
                    subprocess.run([pip_exe, "install", "-r", req_path], check=True, capture_output=True)
                
                # Update command to use venv python
                # command looks like ['python', '-m', 'PyInstaller', ...]
                command[0] = python_exe
                
            self.on_output(f"Comando: {' '.join(command)}\n\n")
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                shell=True
            )
            
            if self.process.stdout:
                for line in self.process.stdout:
                    self.on_output(line)
            
            return_code = self.process.wait()
            self.on_finished(return_code)
            
        except Exception as e:
            self.on_output(f"\nERRO: {str(e)}\n")
            self.on_finished(1)
        finally:
            if temp_dir and os.path.exists(temp_dir):
                self.on_output("\n>>> Limpando ambiente isolado...\n")
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                    self.on_output(">>> Limpeza concluída.\n")
                except Exception as e:
                    self.on_output(f">>> Erro na limpeza: {e}\n")

    def stop(self):
        if self.process:
            self.process.terminate()
