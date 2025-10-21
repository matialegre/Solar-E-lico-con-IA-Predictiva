"""
Script para iniciar el Sistema Inversor Híbrido
Inicia backend y frontend en procesos separados
"""
import subprocess
import os
import sys
import time
import json
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}{Colors.GREEN}🔋 SISTEMA INVERSOR HÍBRIDO - INICIAR{Colors.END}")
    print("=" * 70 + "\n")

def check_ports():
    """Verificar si los puertos están en uso"""
    import socket
    
    ports = {8801: "Backend", 3002: "Frontend"}
    ports_in_use = []
    
    for port, name in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            ports_in_use.append(f"{name} (puerto {port})")
    
    return ports_in_use

def save_pids(backend_pid, frontend_pid):
    """Guardar PIDs en archivo para poder cerrarlos después"""
    pids = {
        'backend': backend_pid,
        'frontend': frontend_pid,
        'timestamp': time.time()
    }
    
    with open('.system_pids.json', 'w') as f:
        json.dump(pids, f, indent=2)
    
    print(f"{Colors.GREEN}✅ PIDs guardados en .system_pids.json{Colors.END}")

def start_backend():
    """Iniciar backend FastAPI"""
    print(f"{Colors.BLUE}🚀 Iniciando Backend (FastAPI)...{Colors.END}")
    
    backend_dir = Path(__file__).parent / "backend"
    
    # Crear proceso en segundo plano
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8801", "--reload"],
        cwd=str(backend_dir),
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"{Colors.GREEN}✅ Backend iniciado (PID: {process.pid}){Colors.END}")
    print(f"   URL: http://localhost:8801")
    
    return process

def start_frontend():
    """Iniciar frontend React"""
    print(f"\n{Colors.BLUE}🚀 Iniciando Frontend (React)...{Colors.END}")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Crear proceso en segundo plano
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=str(frontend_dir),
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"{Colors.GREEN}✅ Frontend iniciado (PID: {process.pid}){Colors.END}")
    print(f"   URL: http://localhost:3002")
    
    return process

def main():
    try:
        print_header()
        
        # Verificar si los puertos están en uso
        print(f"{Colors.YELLOW}🔍 Verificando puertos...{Colors.END}")
        ports_in_use = check_ports()
        
        if ports_in_use:
            print(f"\n{Colors.RED}❌ Los siguientes servicios ya están corriendo:{Colors.END}")
            for service in ports_in_use:
                print(f"   • {service}")
            print(f"\n{Colors.YELLOW}💡 Ejecuta 'python stop_system.py' primero para detenerlos.{Colors.END}\n")
            return
        
        # Iniciar backend
        backend_process = start_backend()
        time.sleep(3)  # Esperar a que backend inicie
        
        # Iniciar frontend
        frontend_process = start_frontend()
        
        # Guardar PIDs
        save_pids(backend_process.pid, frontend_process.pid)
        
        print("\n" + "=" * 70)
        print(f"{Colors.BOLD}{Colors.GREEN}✅ SISTEMA INICIADO CORRECTAMENTE{Colors.END}")
        print("=" * 70)
        print(f"\n{Colors.BOLD}📱 Accede al dashboard:{Colors.END}")
        print(f"   {Colors.BLUE}http://localhost:3002{Colors.END}")
        print(f"\n{Colors.BOLD}📊 API Backend:{Colors.END}")
        print(f"   {Colors.BLUE}http://localhost:8801/docs{Colors.END}")
        print(f"\n{Colors.YELLOW}💡 Para detener el sistema: python stop_system.py{Colors.END}\n")
        
        # Mantener script corriendo para mostrar estado
        print(f"{Colors.YELLOW}Presiona Ctrl+C para salir (los servicios seguirán corriendo)...{Colors.END}\n")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Saliendo... (servicios siguen corriendo){Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
