import subprocess
import argparse

# Configuración del analizador de argumentos
parser = argparse.ArgumentParser(description='Realizar escaneo de puertos de una dirección IP.')
parser.add_argument('ip_address', metavar='IP', type=str, help='La dirección IP a escanear')

args = parser.parse_args()

# Intento de importar la librería nmap y manejar la posible falta de instalación
try:
    import nmap
except ImportError:
    print("Instalando la librería python-nmap...")
    try:
        subprocess.check_call(['pip', 'install', 'python-nmap'])
        print("La librería python-nmap ha sido instalada.")
        import nmap
    except subprocess.CalledProcessError:
        print("Error al instalar la librería python-nmap, por favor instálala manualmente.")
        exit(1)

# Función para escanear puertos
def scan_ports(ip_address):
    nm = nmap.PortScanner()
    nm.scan(ip_address)
    hosts = nm.all_hosts()
    print("IP objetivo:", ip_address)

    for host in hosts:
        estado = "Levantado" if nm[host].state() == 'up' else "Apagado"
        print("Estado de", host, ":", estado)
       
        protocols = nm[host].all_protocols()
        for protocol in protocols:
            print("Protocolo:", protocol)

            open_ports = list(nm[host][protocol].keys())
            for port in open_ports:
                print(f"Puerto {port} abierto en protocolo {protocol}")

# Ejecución del escaneo
target_ip = args.ip_address
scan_ports(target_ip)
