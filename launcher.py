"""
Sistema Inversor Híbrido - Launcher Automático
Inicia backend, frontend y ngrok automáticamente
"""

import subprocess
import time
import sys
import os
import platform
from pathlib import Path

class SystemLauncher:
    def __init__(self):
        self.processes = []
        self.base_path = Path(__file__).parent
        self.is_windows = platform.system() == "Windows"
        
    def print_header(self):
        print("=" * 60)
        print("🚀 SISTEMA INVERSOR HÍBRIDO - LAUNCHER AUTOMÁTICO")
        print("=" * 60)
        print()
    
    def check_dependencies(self):
        """Verificar que todo esté instalado"""
        print("📋 Verificando dependencias...")
        
        # Python
        try:
            import uvicorn
            print("✅ Python y uvicorn instalados")
        except ImportError:
            print("❌ Falta uvicorn. Instalando...")
            subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn"])
        
        # Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js instalado: {result.stdout.strip()}")
            else:
                print("❌ Node.js no encontrado")
                return False
        except FileNotFoundError:
            print("❌ Node.js no encontrado")
            return False
        
        # ngrok
        try:
            result = subprocess.run(["ngrok", "version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ ngrok instalado")
            else:
                print("⚠️  ngrok no encontrado (opcional)")
        except FileNotFoundError:
            print("⚠️  ngrok no encontrado (opcional)")
        
        print()
        return True
    
    def start_backend(self):
        """Iniciar backend FastAPI"""
        print("🖥️  Iniciando Backend (puerto 11113)...")
        
        backend_path = self.base_path / "backend"
        
        if self.is_windows:
            cmd = [
                sys.executable, "-m", "uvicorn", "main:app",
                "--host", "0.0.0.0",
                "--port", "11113",
                "--reload"
            ]
            process = subprocess.Popen(
                cmd,
                cwd=backend_path,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            cmd = [
                sys.executable, "-m", "uvicorn", "main:app",
                "--host", "0.0.0.0",
                "--port", "11113",
                "--reload"
            ]
            process = subprocess.Popen(cmd, cwd=backend_path)
        
        self.processes.append(("Backend", process))
        time.sleep(5)
        print("✅ Backend iniciado")
        print()
    
    def start_frontend(self):
        """Iniciar frontend React"""
        print("🎨 Iniciando Frontend (puerto 3002)...")
        
        frontend_path = self.base_path / "frontend"
        
        if self.is_windows:
            cmd = ["npm", "start"]
            process = subprocess.Popen(
                cmd,
                cwd=frontend_path,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                shell=True
            )
        else:
            cmd = ["npm", "start"]
            process = subprocess.Popen(cmd, cwd=frontend_path, shell=True)
        
        self.processes.append(("Frontend", process))
        time.sleep(8)
        print("✅ Frontend iniciado")
        print()
    
    def start_ngrok(self):
        """Iniciar ngrok para acceso remoto"""
        print("🌐 Iniciando ngrok...")
        
        try:
            if self.is_windows:
                cmd = ["ngrok", "http", "3002", "--domain=argentina.ngrok.pro"]
                process = subprocess.Popen(
                    cmd,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                cmd = ["ngrok", "http", "3002", "--domain=argentina.ngrok.pro"]
                process = subprocess.Popen(cmd)
            
            self.processes.append(("Ngrok", process))
            time.sleep(3)
            print("✅ Ngrok iniciado")
            print()
        except FileNotFoundError:
            print("⚠️  ngrok no encontrado, saltando...")
            print()
    
    def show_urls(self):
        """Mostrar URLs de acceso"""
        print("=" * 60)
        print("🎯 URLS DE ACCESO:")
        print("=" * 60)
        print()
        print("📱 LOCAL:")
        print(f"   Dashboard:  http://localhost:3002")
        print(f"   API Docs:   http://localhost:11113/docs")
        print()
        print("🌐 RED LOCAL:")
        print(f"   Dashboard:  http://190.211.201.217:3002")
        print(f"   API:        http://190.211.201.217:11113")
        print()
        print("☁️  INTERNET (Ngrok):")
        print(f"   Dashboard:  https://argentina.ngrok.pro")
        print()
        print("=" * 60)
        print()
    
    def wait_for_shutdown(self):
        """Esperar a que el usuario cierre"""
        print("✅ SISTEMA COMPLETAMENTE INICIADO")
        print()
        print("📊 Estado:")
        print("   - Backend:  Corriendo en puerto 11113")
        print("   - Frontend: Corriendo en puerto 3002")
        print("   - Ngrok:    Túnel activo")
        print()
        print("💡 Para detener todo, presiona Ctrl+C")
        print()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print()
            print("🛑 Deteniendo sistema...")
            self.cleanup()
    
    def cleanup(self):
        """Limpiar procesos al cerrar"""
        for name, process in self.processes:
            try:
                print(f"   Cerrando {name}...")
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        
        print()
        print("✅ Sistema detenido correctamente")
        print()
    
    def run(self):
        """Ejecutar launcher completo"""
        try:
            self.print_header()
            
            if not self.check_dependencies():
                print("❌ Faltan dependencias. Instala Node.js y Python.")
                return
            
            self.start_backend()
            self.start_frontend()
            self.start_ngrok()
            self.show_urls()
            self.wait_for_shutdown()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.cleanup()
            sys.exit(1)


if __name__ == "__main__":
    launcher = SystemLauncher()
    launcher.run()
