#!/usr/bin/env python3
import os
import sys
import logging
import colorama
from colorama import Fore, Style
from cryptography.fernet import Fernet

from EmbedExtract import Cryptography, Compressor, EmbedExtract  # Import your class code
# Example: from core.EmbedExtract import Cryptography, Compressor, EmbedExtract

colorama.init(autoreset=True)

# ---------- Logging Setup ----------
logging.basicConfig(
    filename='embed_extract.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def print_banner():
    banner_text = f\"\"\"{Fore.CYAN}
    *******************************************
    *     Welcome to the EmbedExtract Menu    *
    *******************************************
    {Style.RESET_ALL}\"\"\"
    print(banner_text)

def main_menu():
    print(f\"{Fore.GREEN}Available Operations:\")
    print(f\"{Fore.YELLOW}[1]{Style.RESET_ALL} Embed Data in JPEG/PNG/GIF\")
    print(f\"{Fore.YELLOW}[2]{Style.RESET_ALL} Extract Data from JPEG/PNG/GIF\")
    print(f\"{Fore.YELLOW}[3]{Style.RESET_ALL} Embed Data in PDF Metadata\")
    print(f\"{Fore.YELLOW}[4]{Style.RESET_ALL} Extract Data from PDF Metadata\")
    print(f\"{Fore.YELLOW}[5]{Style.RESET_ALL} Create QR Code\")
    print(f\"{Fore.YELLOW}[6]{Style.RESET_ALL} Decode QR Code\")
    print(f\"{Fore.YELLOW}[7]{Style.RESET_ALL} Exit\")

def get_format_choice():
    print(\"\\nChoose image format:\")
    print(\"  1. JPEG\")
    print(\"  2. PNG\")
    print(\"  3. GIF\")
    choice = input(\"Enter your choice (1-3): \").strip()
    if choice == '1':
        return 'jpeg'
    elif choice == '2':
        return 'png'
    elif choice == '3':
        return 'gif'
    else:
        print(f\"{Fore.RED}Invalid choice.\")
        return None

def run_menu():
    embed_extract = EmbedExtract()
    crypto = Cryptography()
    compressor = Compressor()

    while True:
        main_menu()
        choice = input(\"\\nSelect an option (1-7): \").strip()

        if choice == '1':
            file_format = get_format_choice()
            if not file_format:
                continue
            carrier_path = input(\"Enter the carrier file path: \").strip()
            payload_path = input(\"Enter the payload file path: \").strip()
            if not (os.path.isfile(carrier_path) and os.path.isfile(payload_path)):
                print(f\"{Fore.RED}Invalid file paths.\")
                continue

            # Encryption and compression options
            enc_choice = input(\"Encrypt data? (y/n): \").lower()
            comp_choice = input(\"Compress data? (y/n): \").lower()

            try:
                with open(payload_path, 'rb') as f:
                    data = f.read()

                if comp_choice == 'y':
                    data = compressor.compress(data)
                    logging.info(\"Data compressed.\")
                if enc_choice == 'y':
                    data = crypto.encrypt(data)
                    logging.info(\"Data encrypted.\")
                
                success = embed_extract.embed_binary(carrier_path, data, file_format)
                if success:
                    print(f\"{Fore.GREEN}Data successfully embedded.\")
                    logging.info(\"Embed operation successful.\")
                else:
                    print(f\"{Fore.RED}Embed operation failed.\")
                    logging.error(\"Embed operation failed.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception in embed operation\")

        elif choice == '2':
            file_format = get_format_choice()
            if not file_format:
                continue
            carrier_path = input(\"Enter the carrier file path: \").strip()
            if not os.path.isfile(carrier_path):
                print(f\"{Fore.RED}Invalid file path.\")
                continue

            output_path = input(\"Enter the output path (to save extracted data): \").strip()
            enc_choice = input(\"Data was encrypted? (y/n): \").lower()
            comp_choice = input(\"Data was compressed? (y/n): \").lower()

            try:
                data = embed_extract.extract_binary(carrier_path, file_format)
                if data is None:
                    print(f\"{Fore.RED}No data found or error in extraction.\")
                    logging.error(\"Extract operation failed.\")
                    continue

                if enc_choice == 'y':
                    data = crypto.decrypt(data)
                    logging.info(\"Data decrypted.\")
                if comp_choice == 'y':
                    data = compressor.decompress(data)
                    logging.info(\"Data decompressed.\")

                with open(output_path, 'wb') as f:
                    f.write(data)

                print(f\"{Fore.GREEN}Data extracted and saved to {output_path}.\")
                logging.info(\"Extract operation successful.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception in extract operation\")

        elif choice == '3':
            pdf_path = input(\"Enter the PDF path: \").strip()
            if not os.path.isfile(pdf_path):
                print(f\"{Fore.RED}Invalid file path.\")
                continue
            data_file = input(\"Enter file containing data to embed: \").strip()
            if not os.path.isfile(data_file):
                print(f\"{Fore.RED}Invalid file path.\")
                continue

            enc_choice = input(\"Encrypt data? (y/n): \").lower()
            comp_choice = input(\"Compress data? (y/n): \").lower()

            try:
                with open(data_file, 'rb') as f:
                    data = f.read()

                if comp_choice == 'y':
                    data = compressor.compress(data)
                    logging.info(\"Data compressed.\")
                if enc_choice == 'y':
                    data = crypto.encrypt(data)
                    logging.info(\"Data encrypted.\")

                success = embed_extract.embed_pdf(pdf_path, data)
                if success:
                    print(f\"{Fore.GREEN}Data embedded in PDF metadata.\")
                    logging.info(\"PDF embed operation successful.\")
                else:
                    print(f\"{Fore.RED}PDF embed failed.\")
                    logging.error(\"PDF embed operation failed.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception in PDF embed operation\")

        elif choice == '4':
            pdf_path = input(\"Enter the PDF path: \").strip()
            if not os.path.isfile(pdf_path):
                print(f\"{Fore.RED}Invalid file path.\")
                continue
            output_file = input(\"Enter output file to save extracted data: \").strip()

            enc_choice = input(\"Data was encrypted? (y/n): \").lower()
            comp_choice = input(\"Data was compressed? (y/n): \").lower()

            try:
                data = embed_extract.extract_pdf(pdf_path)
                if not data:
                    print(f\"{Fore.RED}No data found or error in extraction.\")
                    logging.error(\"PDF extract operation failed.\")
                    continue
                if enc_choice == 'y':
                    data = crypto.decrypt(data)
                    logging.info(\"PDF data decrypted.\")
                if comp_choice == 'y':
                    data = compressor.decompress(data)
                    logging.info(\"PDF data decompressed.\")

                with open(output_file, 'wb') as f:
                    f.write(data)

                print(f\"{Fore.GREEN}Data extracted from PDF and saved to {output_file}.\")
                logging.info(\"PDF extract operation successful.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception in PDF extract operation\")

        elif choice == '5':
            data = input(\"Enter the data for the QR code: \").strip()
            output_file = input(\"Enter the output filename (e.g. qrcode.png): \").strip()
            try:
                embed_extract.create_qr(data, output_file)
                print(f\"{Fore.GREEN}QR code created and saved to {output_file}.\")
                logging.info(\"QR code creation successful.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception in QR creation\")

        elif choice == '6':
            qr_file = input(\"Enter the path to the QR image: \").strip()
            if not os.path.isfile(qr_file):
                print(f\"{Fore.RED}Invalid file path.\")
                continue
            try:
                decoded_data = embed_extract.decode_qr(qr_file)
                if decoded_data:
                    print(f\"{Fore.GREEN}Decoded Data: {decoded_data.decode('utf-8')}\")
                    logging.info(\"QR code decode successful.\")
                else:
                    print(f\"{Fore.RED}No data found in QR code.\")
                    logging.warning(\"QR code decode found no data.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception in QR decoding\")

        elif choice == '7':
            print(f\"{Fore.CYAN}Exiting. Goodbye!\")
            sys.exit(0)
        else:
            print(f\"{Fore.RED}Invalid choice. Please try again.\")

def main():
    print_banner()
    run_menu()

if __name__ == \"__main__\":
    main()
