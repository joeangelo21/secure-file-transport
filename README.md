# Secure File Transport (Secure-File-Transport)

A high-assurance, end-to-end file transfer utility engineered for secure peer-to-peer data transmission across network environments.

## 🛡️ Key Features

- **Memory-Optimized Stream Handling:** Compresses targets directly into memory (`io.BytesIO`) using `tar.gz` formats, preventing unnecessary disk I/O bottlenecks.
- **TCP Socket Streaming:** Utilizes robust stream sockets with configurable chunk sizes (64 KB) for high-throughput performance.
- **Real-Time Progress Tracking:** Live feedback with percentage and megabyte throughput metrics during transmission and extraction.
- **Dual Operating Modes:** Functions seamlessly as an active transmitter (Client) or an asynchronous receiver (Server).
- **CLI & Interactive Support:** Fully operable via standard command-line arguments (`argparse`) or a built-in guided interactive menu.

## 🚀 Architecture & Workflow

1. **Compression Phase:** The client targets a specified file or directory, packaging it in-memory into a compressed tar archive.
2. **Socket Initialization:** Establishes a reliable TCP connection with the destination listener.
3. **Stream Transmission:** Data is streamed in structured chunks with real-time progress calculations.
4. **Extraction Phase:** The server receives the binary stream, reconstructs the buffer, and securely unpacks payloads to the designated output directory.

## 🛠️ Usage

### Command-Line Interface (CLI)

- **Server Mode (Receiver):**
  ```bash
  python3 transport.py --listen --port 4444 --output ./received_files

    Client Mode (Sender):
    Bash

    python3 transport.py --target /path/to/payload --ip <DESTINATION_IP> --port 4444

Interactive Mode

Execute the script without arguments to launch the guided prompt:
Bash

python3 transport.py

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.


