# ddos-simulation_botnet

## Project Overview

This project demonstrates the development and deployment of a master bot and subordinate bots to simulate Distributed Denial of Service (DDoS) attacks within a Local Area Network (LAN). The project is intended for educational purposes to understand the mechanics of DDoS attacks and botnet behavior.

## Prerequisites

1. Python 3.x
2. Required Python libraries:
    - `socket`
    - `ssl`
    - `threading`
    - `colorama`
    - `requests`
    - `scapy`
    - `logging`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/tsharbi/ddos-simulation_botnet.git
    cd ddos-simulation_botnet
    ```

2. Install the required Python libraries:
    ```bash
    pip install colorama requests scapy
    ```

3. Generate SSL certificates:
    ```bash
    openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
    ```

## Running the Master Bot

```bash
python master_bot.py
```

## Running the Bots
```bash
python bot.py
```

## Features

- **Master Bot**:
  - Acts as the command-and-control center.
  - Lists connected bots.
  - Executes various DDoS attacks:
    - ICMP flood attack
    - SYN flood attack
    - UDP flood attack
  - Stops ongoing DDoS attacks.
  - Secure communication using SSL/TLS.

- **Subordinate Bots**:
  - Establish secure connections with the master bot.
  - Execute DDoS attacks on command from the master bot.
 
## Example of Master Bot Interface

Here is an example of the Master Bot interface:
![Master Bot Interface]  (https://github.com/tsharbi/ddos-simulation_botnet/assets/66922177/f809241b-360a-46bc-9ffa-3445e90ac3d3)
 

## Disclaimer

This project is intended solely for educational purposes to understand DDoS attack mechanisms and botnet behavior. Use this code only in a controlled environment and with proper authorization.

