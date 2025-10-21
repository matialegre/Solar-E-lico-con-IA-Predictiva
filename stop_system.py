"""
Script para detener el Sistema Inversor Híbrido
Detiene solo los procesos del sistema sin afectar otros
"""
import json
import os
import sys
import psutil
import time

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
    print(f"{Colors.BOLD}{Colors.RED}🛑 SISTEMA INVERSOR HÍBRIDO - DETENER{Colors.END}")
    print("=" * 70 + "\n")

def load_pids():
    """Cargar PIDs guardados"""
    if not os.path.exists('.system_pids.json'):
        return None
    
    try:
        with open('.system_pids.json', 'r') as f:
            return json.load(f)
    except:
        return None

def kill_process_tree(pid):
    """Matar proceso y todos sus hijos"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # Primero terminar hijos
        for child in children:
            try:
                print(f"   └─ Deteniendo proceso hijo (PID: {child.pid})")
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        
        # Esperar terminación
        gone, alive = psutil.wait_procs(children, timeout=3)
        
        # Forzar si no terminaron
        for p in alive:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
        
        # Terminar padre
        try:
            parent.terminate()
            parent.wait(timeout=3)
        except psutil.TimeoutExpired:
            parent.kill()
        except psutil.NoSuchProcess:
            pass
        
        return True
        
    except psutil.NoSuchProcess:
        return False
    except Exception as e:
        print(f"{Colors.RED}   Error: {e}{Colors.END}")
        return False

def stop_by_pids(pids_data):
    """Detener procesos usando PIDs guardados"""
    stopped = []
    
    if pids_data.get('backend'):
        print(f"{Colors.YELLOW}🔄 Deteniendo Backend (PID: {pids_data['backend']})...{Colors.END}")
        if kill_process_tree(pids_data['backend']):
            stopped.append('Backend')
            print(f"{Colors.GREEN}✅ Backend detenido{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠️  Backend no encontrado (ya estaba detenido){Colors.END}")
    
    if pids_data.get('frontend'):
        print(f"\n{Colors.YELLOW}🔄 Deteniendo Frontend (PID: {pids_data['frontend']})...{Colors.END}")
        if kill_process_tree(pids_data['frontend']):
            stopped.append('Frontend')
            print(f"{Colors.GREEN}✅ Frontend detenido{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠️  Frontend no encontrado (ya estaba detenido){Colors.END}")
    
    return stopped

def stop_by_port_scan():
    """Buscar y detener procesos en puertos conocidos"""
    import socket
    
    print(f"{Colors.YELLOW}🔍 Buscando procesos en puertos del sistema...{Colors.END}\n")
    
    ports = {8801: "Backend", 3002: "Frontend"}
    stopped = []
    
    for port, name in ports.items():
        # Verificar si el puerto está en uso
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            # Puerto en uso, buscar proceso
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    connections = proc.info['connections']
                    if connections:
                        for conn in connections:
                            if hasattr(conn, 'laddr') and conn.laddr.port == port:
                                print(f"{Colors.YELLOW}🔄 Deteniendo {name} (PID: {proc.pid})...{Colors.END}")
                                kill_process_tree(proc.pid)
                                stopped.append(name)
                                print(f"{Colors.GREEN}✅ {name} detenido{Colors.END}\n")
                                break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
    
    return stopped

def cleanup_pid_file():
    """Eliminar archivo de PIDs"""
    if os.path.exists('.system_pids.json'):
        os.remove('.system_pids.json')
        print(f"{Colors.GREEN}✅ Archivo de PIDs eliminado{Colors.END}")

def main():
    try:
        print_header()
        
        # Intentar detener por PIDs guardados
        pids_data = load_pids()
        stopped = []
        
        if pids_data:
            print(f"{Colors.BLUE}📋 Usando PIDs guardados...{Colors.END}\n")
            stopped = stop_by_pids(pids_data)
            cleanup_pid_file()
        else:
            print(f"{Colors.YELLOW}⚠️  No se encontró archivo de PIDs{Colors.END}")
        
        # Si no se detuvo nada, buscar por puertos
        if not stopped:
            print(f"\n{Colors.BLUE}🔍 Método alternativo: Búsqueda por puertos...{Colors.END}\n")
            stopped = stop_by_port_scan()
        
        # Resultado final
        print("\n" + "=" * 70)
        if stopped:
            print(f"{Colors.BOLD}{Colors.GREEN}✅ SISTEMA DETENIDO CORRECTAMENTE{Colors.END}")
            print("=" * 70)
            print(f"\n{Colors.GREEN}Servicios detenidos:{Colors.END}")
            for service in stopped:
                print(f"   ✓ {service}")
        else:
            print(f"{Colors.BOLD}{Colors.YELLOW}⚠️  NINGÚN SERVICIO ENCONTRADO{Colors.END}")
            print("=" * 70)
            print(f"\n{Colors.YELLOW}El sistema probablemente no estaba corriendo.{Colors.END}")
        
        print(f"\n{Colors.BLUE}💡 Para iniciar nuevamente: python start_system.py{Colors.END}\n")
        
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
