# Network Security Simulations

## Project Overview
This project is designed to simulate and analyze different types of network attacks, specifically ICMP Flood Attacks, SYN Flood Attacks, and Regex Injection Attacks. It also demonstrates effective mitigation techniques to protect systems against these threats. This tool is intended strictly for educational purposes or authorized security testing.

## Prerequisites
To run this project, you will need:
- Python 3.x
- Flask
- Requests
- memory_profiler
- Flask-Limiter

Ensure all tools and libraries are installed using pip:

```bash
pip install flask requests memory_profiler flask-limiter
```
## Installation
Clone the repository to your local machine:
```bash
git clone <repository-url>
cd <project-directory>
```
## Usage
Running the Flask App
Start the Flask application by running:
```bash
python app.py
```
# Simulating Network Attacks
The project includes scripts to simulate the following attacks:
ICMP Flood Attack: Generates a high volume of ICMP packets to overwhelm the target system.
```bash
python icmp_flood_attack.py <Target-IP>
```
SYN Flood Attack: Initiates a large number of SYN requests to exhaust server resources.
```bash
bash syn_flood_attack.sh
```
ReDoS attack, or Regular Expression Injection Attack: Tests the system's handling of specially crafted input designed to exploit regex vulnerabilities.

# Start in another terminal while the Flask app is running
```bash
python inject_traffic.py
```
# Ethical Considerations
Ensure that all testing is conducted in a controlled environment, such as a lab setup or with explicit permission from the network owners. Unauthorized testing on networks not owned by you is illegal and unethical.
