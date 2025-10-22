"""
Sistema Inversor Híbrido - Iniciador Automático con HTTPS
Levanta backend, frontend y configura ngrok automáticamente
"""

import subprocess
import time
import os
import sys
import requests
import json
from pathlib import Path

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def kill_processes():
    """Matar procesos previos"""
    print_info("Limpiando procesos anteriores...")
    
    processes = ['node.exe', 'python.exe', 'ngrok.exe', 'uvicorn']
    for proc in processes:
        try:
            subprocess.run(['taskkill', '/F', '/IM', proc], 
                         capture_output=True, shell=True)
        except:
            pass
    
    time.sleep(2)
    print_success("Procesos limpiados")

def start_backend():
    """Iniciar backend FastAPI"""
    print_info("Iniciando Backend (Puerto 11113)...")
    
    backend_dir = Path(__file__).parent / "backend"
    
    if not backend_dir.exists():
        print_error("No se encuentra la carpeta backend/")
        return None
    
    # Iniciar backend en proceso separado
    process = subprocess.Popen(
        ['python', '-m', 'uvicorn', 'main:app', 
         '--host', '0.0.0.0', '--port', '11113', '--reload'],
        cwd=str(backend_dir),
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    time.sleep(8)
    
    # Verificar que esté corriendo
    try:
        response = requests.get('http://localhost:11113/api/system/status', timeout=5)
        if response.status_code == 200:
            print_success("Backend iniciado correctamente")
            return process
    except:
        print_warning("Backend tardando en iniciar, esperando más...")
        time.sleep(5)
    
    return process

def start_ngrok_backend():
    """Iniciar ngrok para el backend"""
    print_info("Creando túnel HTTPS para Backend...")
    
    # Iniciar ngrok en proceso separado
    process = subprocess.Popen(
        ['ngrok', 'http', '11113', '--region', 'sa', '--log', 'stdout'],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    time.sleep(8)
    
    # Obtener URL de ngrok
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.get('http://127.0.0.1:4040/api/tunnels')
            data = response.json()
            
            # Buscar túnel HTTPS
            for tunnel in data.get('tunnels', []):
                public_url = tunnel.get('public_url', '')
                if 'https' in public_url and '11113' in tunnel.get('config', {}).get('addr', ''):
                    print_success(f"Túnel Backend: {public_url}")
                    return process, public_url
            
            time.sleep(2)
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(2)
            else:
                print_error(f"No se pudo obtener URL de ngrok: {e}")
                return None, None
    
    return process, None

def configure_frontend(backend_url):
    """Configurar frontend con URL del backend"""
    print_info("Configurando Frontend...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    env_file = frontend_dir / ".env.local"
    
    with open(env_file, 'w') as f:
        f.write(f"REACT_APP_API_URL={backend_url}\n")
        f.write(f"PORT=3002\n")
    
    print_success(f"Frontend configurado para usar: {backend_url}")

def start_frontend():
    """Iniciar frontend React"""
    print_info("Iniciando Frontend (Puerto 3002)...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print_error("No se encuentra la carpeta frontend/")
        return None
    
    # Iniciar frontend
    env = os.environ.copy()
    env['BROWSER'] = 'none'
    
    process = subprocess.Popen(
        ['npm', 'start'],
        cwd=str(frontend_dir),
        env=env,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    time.sleep(10)
    print_success("Frontend iniciado")
    return process

def start_ngrok_frontend():
    """Iniciar ngrok para el frontend con dominio fijo"""
    print_info("Creando túnel HTTPS para Frontend...")
    
    process = subprocess.Popen(
        ['ngrok', 'http', '3002', '--region', 'sa', '--domain', 'argentina.ngrok.pro'],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    time.sleep(5)
    print_success("Frontend disponible en: https://argentina.ngrok.pro")
    return process

def main():
    """Función principal"""
    print_header("SISTEMA INVERSOR HÍBRIDO - HTTPS AUTOMÁTICO")
    
    try:
        # 1. Limpiar procesos previos
        kill_processes()
        
        # 2. Iniciar backend
        backend_proc = start_backend()
        if not backend_proc:
            print_error("Error al iniciar backend")
            return
        
        # 3. Crear túnel ngrok para backend
        ngrok_backend_proc, backend_url = start_ngrok_backend()
        if not backend_url:
            print_error("Error al crear túnel ngrok del backend")
            return
        
        # 4. Configurar frontend con URL del backend
        configure_frontend(backend_url)
        
        # 5. Iniciar frontend
        frontend_proc = start_frontend()
        if not frontend_proc:
            print_error("Error al iniciar frontend")
            return
        
        # 6. Crear túnel ngrok para frontend
        ngrok_frontend_proc = start_ngrok_frontend()
        
        # Resumen final
        print_header("✅ SISTEMA INICIADO EXITOSAMENTE")
        print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}🔧 Backend HTTPS:{Colors.ENDC}  {backend_url}")
        print(f"{Colors.BOLD}🌐 Frontend HTTPS:{Colors.ENDC} https://argentina.ngrok.pro")
        print(f"{Colors.BOLD}📊 Panel Ngrok:{Colors.ENDC}    http://localhost:4040")
        print(f"{Colors.BOLD}📝 API Docs:{Colors.ENDC}       {backend_url}/docs")
        print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}✅ Sin errores de Mixed Content{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✅ Todas las conexiones son HTTPS{Colors.ENDC}\n")
        
        # Abrir navegador
        print_info("Abriendo dashboard...")
        time.sleep(2)
        os.system('start https://argentina.ngrok.pro')
        
        print(f"\n{Colors.WARNING}Presiona Ctrl+C para detener el sistema{Colors.ENDC}\n")
        
        # Mantener el script corriendo
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print_info("\nDeteniendo sistema...")
            kill_processes()
            print_success("Sistema detenido")
    
    except Exception as e:
        print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
