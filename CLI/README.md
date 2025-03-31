# Steganography Tool CLI

## Overview
The `CLI/main.py` file in the `Steganography-Tool` repository provides a command-line interface (CLI) for embedding and extracting data within various file formats. This tool supports operations on images (JPEG, PNG, GIF), PDFs, and QR codes, with optional encryption and compression of data.

## Features
- **Embed and Extract Data in Images**: Supports JPEG, PNG, and GIF formats.
- **Embed and Extract Data in PDF Metadata**: Allows embedding and extraction of data within PDF metadata.
- **QR Code Operations**: Create and decode QR codes.
- **Optional Encryption and Compression**: Data can be encrypted and/or compressed before embedding.

## Dependencies
- Python 3.x
- `colorama` for colored terminal text
- `cryptography` for data encryption
- `EmbedExtract`, `Cryptography`, and `Compressor` classes for steganographic operations (assumed to be part of the project)

## Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/elithaxxor/Steganography-Tool.git
    cd Steganography-Tool/CLI
    ```
2. Install the required Python packages:
    ```sh
    pip install colorama cryptography
    ```

## Usage
Run the `main.py` file to start the CLI:
```sh
python main.py
