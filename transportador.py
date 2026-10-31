#!/usr/bin/env python3
"""
Secure File Transport CLI - Peer-to-Peer File Transfer Utility
Author: Joelson Angelo (joeangelo21)
"""

import os
import socket
import tarfile
import io
import sys
import argparse

CHUNK_SIZE = 65536  # 64 KB

def server_mode(port: int, destination_dir: str = ".") -> None:
    """Receiver mode: listens for incoming connections and extracts the tar.gz payload."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', port))
            s.listen(1)
            print(f"\n[*] Server listening on 0.0.0.0:{port}...")

            conn, addr = s.accept()
            print(f"[+] Connection established with {addr[0]}:{addr[1]}")

            buffer = io.BytesIO()
            with conn:
                received_bytes = 0
                while True:
                    data = conn.recv(CHUNK_SIZE)
                    if not data:
                        break
                    buffer.write(data)
                    received_bytes += len(data)
                    print(f"\r[*] Receiving payload: {received_bytes / (1024*1024):.2f} MB", end="")

                print("\n[+] Transfer complete. Extracting archives...")
                buffer.seek(0)
                try:
                    with tarfile.open(fileobj=buffer, mode="r:gz") as tar:
                        tar.extractall(path=destination_dir)
                    print(f"[+] Payload successfully extracted to '{os.path.abspath(destination_dir)}'!")
                except Exception as e:
                    print(f"\n[!] Extraction error: {e}")

    except KeyboardInterrupt:
        print("\n[!] Server interrupted by user.")
    except Exception as e:
        print(f"\n[!] Server error: {e}")

def client_mode(target_path: str, destination_ip: str, port: int) -> None:
    """Sender mode: compresses target in memory and streams via socket."""
    if not os.path.exists(target_path):
        print(f"\n[!] Error: Target path '{target_path}' does not exist.")
        return

    print(f"\n[*] Compressing '{target_path}' in memory...")
    buffer = io.BytesIO()
    try:
        with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
            tar.add(target_path, arcname=os.path.basename(target_path))
    except Exception as e:
        print(f"[!] Compression error: {e}")
        return

    total_size = buffer.tell()
    buffer.seek(0)
    print(f"[+] Payload generated: {total_size / (1024*1024):.2f} MB")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"[*] Connecting to destination {destination_ip}:{port}...")
            s.connect((destination_ip, port))

            sent_bytes = 0
            while chunk := buffer.read(CHUNK_SIZE):
                s.sendall(chunk)
                sent_bytes += len(chunk)
                progress = (sent_bytes / total_size) * 100
                print(f"\r[*] Transmitting: {progress:.1f}% ({sent_bytes / (1024*1024):.2f} MB)", end="")

            print(f"\n[+] '{target_path}' successfully transmitted!")

    except ConnectionRefusedError:
        print("\n[!] Error: Connection refused. Verify if the target listener is active and the port is open.")
    except Exception as e:
        print(f"\n[!] Transmission error: {e}")

def interactive_menu() -> None:
    """Terminal interactive menu when executed without arguments."""
    print("=" * 50)
    print("        SECURE FILE TRANSPORT - P2P")
    print("=" * 50)
    print("[ 1 ] Send file or directory (Client Mode)")
    print("[ 2 ] Listen and receive payload (Server Mode)")
    print("=" * 50)

    option = input("Select an option (1 or 2): ").strip()

    if option == '1':
        target = input("\n[?] Target file or directory to send: ").strip('"\' ')
        ip = input("[?] Destination IP address: ").strip()
        port_str = input("[?] Destination port (Default: 4444): ").strip()
        port = int(port_str) if port_str else 4444

        if target and ip:
            client_mode(target, ip, port)
        else:
            print("[!] Error: Target path and destination IP are required.")

    elif option == '2':
        port_str = input("\n[?] Listen port (Default: 4444): ").strip()
        port = int(port_str) if port_str else 4444
        destination = input("[?] Output directory for received files (Default '.'): ").strip()
        destination = destination if destination else "."

        server_mode(port, destination)
    else:
        print("[!] Invalid option. Exiting.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Secure File Transport CLI - TCP Socket File Transfer Utility")
    parser.add_argument("-l", "--listen", action="store_true", help="Enable server mode (receiver)")
    parser.add_argument("-t", "--target", type=str, help="Target file or folder to transmit")
    parser.add_argument("-i", "--ip", type=str, help="Destination server IP address")
    parser.add_argument("-p", "--port", type=int, default=4444, help="TCP port (default: 4444)")
    parser.add_argument("-o", "--output", type=str, default=".", help="Output directory for received payloads")

    args = parser.parse_args()

    if args.listen:
        server_mode(args.port, args.output)
    elif args.target and args.ip:
        client_mode(args.target, args.ip, args.port)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
