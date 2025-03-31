#!/usr/bin/env python3
import os
import sys
import zlib
import logging
import traceback

# Cryptography
from cryptography.fernet import Fernet

# PDFs
from PyPDF2 import PdfReader, PdfWriter

# Images & QR
from PIL import Image
import qrcode
from pyzbar.pyzbar import decode

# Colorful CLI
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


## pip install colorama cryptography PyPDF2 qrcode pyzbar pillow

#####################################################
#                   CLASSES                         #
#####################################################

class Cryptography:
    def __init__(self, key=None):
        # Generate a new key if one isn't provided
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: bytes) -> bytes:
        return self.cipher.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        return self.cipher.decrypt(data)


class Compressor:
    @staticmethod
    def compress(data: bytes) -> bytes:
        return zlib.compress(data)

    @staticmethod
    def decompress(data: bytes) -> bytes:
        return zlib.decompress(data)


class EmbedExtract:
    """
    Provides logic to embed/extract data in:
      - JPEG/PNG/GIF via appending bytes after EOF marker
      - PDF via metadata
      - QR codes (create/ decode)
    """
    EOF_MARKERS = {
        'jpeg': b'\xff\xd9',
        'png': b'IEND\xaeB`\x82',
        'gif': b'\x00;',
    }

    # ---------- Image-based: JPEG, PNG, GIF ----------
    def embed_binary(self, file_path: str, data: bytes, file_format: str) -> bool:
        """Appends data right after the format-specific EOF marker."""
        eof_marker = self.EOF_MARKERS.get(file_format.lower())
        if not eof_marker:
            raise ValueError(f'Unsupported file format: {file_format}')

        try:
            with open(file_path, 'ab') as carrier:
                carrier.write(eof_marker)
                carrier.write(data)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def extract_binary(self, file_path: str, file_format: str) -> bytes:
        """Extracts data appended after the format-specific EOF marker."""
        eof_marker = self.EOF_MARKERS.get(file_format.lower())
        if not eof_marker:
            raise ValueError(f'Unsupported file format: {file_format}')

        try:
            with open(file_path, 'rb') as carrier:
                content = carrier.read()
                offset = content.index(eof_marker) + len(eof_marker)
                return content[offset:]
        except Exception:
            traceback.print_exc()
            return None

    # ---------- PDF-based metadata ----------
    def embed_pdf(self, pdf_path: str, data: bytes) -> bool:
        """
        Embeds the given data into PDF metadata field /HiddenData.
        By convention, store data as text => data.decode('utf-8')
        """
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            # Store the data in metadata as string
            # Make sure to store as something that won't break PDF if it's binary
            text_data = data.decode('utf-8', errors='replace')
            writer.add_metadata({"/HiddenData": text_data})

            base_name = os.path.basename(pdf_path)
            new_pdf_path = f"embedded_{base_name}"

            with open(new_pdf_path, 'wb') as out_pdf:
                writer.write(out_pdf)

            return True
        except Exception:
            traceback.print_exc()
            return False

    def extract_pdf(self, pdf_path: str) -> bytes:
        """Reads the hidden data from PDF metadata field /HiddenData."""
        try:
            reader = PdfReader(pdf_path)
            metadata = reader.metadata
            hidden_data = metadata.get("/HiddenData")
            if not hidden_data:
                return None
            return hidden_data.encode('utf-8')
        except Exception:
            traceback.print_exc()
            return None

    # ---------- QR-based ----------
    def create_qr(self, data: bytes, output_file: str) -> bool:
        """
        Creates a QR code from the given data (assumes ASCII/UTF-8).
        If data is truly binary, base64-encode it before calling this function.
        """
        try:
            # For raw binary data, interpret it as a string
            # or expect that it's pre-decoded or base64.
            # We'll just decode ignoring errors for demonstration.
            text_data = data.decode('utf-8', errors='replace')
            qr_img = qrcode.make(text_data)
            qr_img.save(output_file)
            return True
        except Exception:
            traceback.print_exc()
            return False

    def decode_qr(self, qr_file: str) -> bytes:
        """Decodes a QR code image and returns raw bytes."""
        try:
            img = Image.open(qr_file)
            decoded_info = decode(img)
            if decoded_info:
                return decoded_info[0].data
            return None
        except Exception:
            traceback.print_exc()
            return None


#####################################################
#               LOGGING CONFIGURATION               #
#####################################################

logging.basicConfig(
    filename='embed_extract.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


#####################################################
#                 MENU / CLI LOGIC                  #
#####################################################

def print_banner():
    banner_text = f\"\"\"{Fore.CYAN}
    *******************************************
    *         Welcome to EmbedExtract CLI     *
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

        # 1) Embed Data in JPEG/PNG/GIF
        if choice == '1':
            file_format = get_format_choice()
            if not file_format:
                continue

            carrier_path = input(\"Enter the carrier file path: \").strip()
            if not os.path.isfile(carrier_path):
                print(f\"{Fore.RED}Invalid carrier file.\")
                continue

            payload_path = input(\"Enter the payload file path: \").strip()
            if not os.path.isfile(payload_path):
                print(f\"{Fore.RED}Invalid payload file.\")
                continue

            enc_choice = input(\"Encrypt data? (y/n): \").lower()
            comp_choice = input(\"Compress data? (y/n): \").lower()

            try:
                with open(payload_path, 'rb') as f:
                    data = f.read()

                # Compress
                if comp_choice == 'y':
                    data = compressor.compress(data)
                    logging.info(\"Data compressed.\")

                # Encrypt
                if enc_choice == 'y':
                    data = crypto.encrypt(data)
                    logging.info(\"Data encrypted.\")

                success = embed_extract.embed_binary(carrier_path, data, file_format)
                if success:
                    print(f\"{Fore.GREEN}Data successfully embedded.\")
                    logging.info(\"Image embed operation successful.\")
                else:
                    print(f\"{Fore.RED}Embed operation failed.\")
                    logging.error(\"Embed operation failed.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception during embed operation\")

        # 2) Extract Data from JPEG/PNG/GIF
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
                    logging.error(\"Extract operation returned None.\")
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
                logging.exception(\"Exception during extract operation\")

        # 3) Embed Data in PDF Metadata
        elif choice == '3':
            pdf_path = input(\"Enter the PDF path: \").strip()
            if not os.path.isfile(pdf_path):
                print(f\"{Fore.RED}Invalid PDF path.\")
                continue

            data_path = input(\"Enter file containing data to embed: \").strip()
            if not os.path.isfile(data_path):
                print(f\"{Fore.RED}Invalid data file.\")
                continue

            enc_choice = input(\"Encrypt data? (y/n): \").lower()
            comp_choice = input(\"Compress data? (y/n): \").lower()

            try:
                with open(data_path, 'rb') as f:
                    data = f.read()

                if comp_choice == 'y':
                    data = compressor.compress(data)
                    logging.info(\"PDF data compressed.\")

                if enc_choice == 'y':
                    data = crypto.encrypt(data)
                    logging.info(\"PDF data encrypted.\")

                success = embed_extract.embed_pdf(pdf_path, data)
                if success:
                    print(f\"{Fore.GREEN}Data embedded in PDF metadata.\")
                    logging.info(\"PDF embed operation successful.\")
                else:
                    print(f\"{Fore.RED}PDF embed failed.\")
                    logging.error(\"PDF embed operation failed.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception during PDF embed\")

        # 4) Extract Data from PDF Metadata
        elif choice == '4':
            pdf_path = input(\"Enter the PDF path: \").strip()
            if not os.path.isfile(pdf_path):
                print(f\"{Fore.RED}Invalid PDF path.\")
                continue

            output_file = input(\"Enter output file to save extracted data: \").strip()
            enc_choice = input(\"Data was encrypted? (y/n): \").lower()
            comp_choice = input(\"Data was compressed? (y/n): \").lower()

            try:
                data = embed_extract.extract_pdf(pdf_path)
                if not data:
                    print(f\"{Fore.RED}No data found or error in extraction.\")
                    logging.error(\"PDF extract returned no data.\")
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
                logging.exception(\"Exception during PDF extraction\")

        # 5) Create QR Code
        elif choice == '5':
            data_path = input(\"Enter path to file with data to embed in QR: \").strip()
            if not os.path.isfile(data_path):
                print(f\"{Fore.RED}Invalid data path.\")
                continue

            output_file = input(\"Enter filename for the QR code image (e.g. code.png): \").strip()
            if not output_file:
                print(f\"{Fore.RED}No output file specified.\")
                continue

            enc_choice = input(\"Encrypt data? (y/n): \").lower()
            comp_choice = input(\"Compress data? (y/n): \").lower()

            try:
                with open(data_path, 'rb') as f:
                    data = f.read()

                if comp_choice == 'y':
                    data = compressor.compress(data)
                    logging.info(\"QR data compressed.\")

                if enc_choice == 'y':
                    data = crypto.encrypt(data)
                    logging.info(\"QR data encrypted.\")

                success = embed_extract.create_qr(data, output_file)
                if success:
                    print(f\"{Fore.GREEN}QR code created and saved as {output_file}.\")
                    logging.info(\"QR code creation successful.\")
                else:
                    print(f\"{Fore.RED}QR code creation failed.\")
                    logging.error(\"QR code creation failed.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception in QR creation\")

        # 6) Decode QR Code
        elif choice == '6':
            qr_file = input(\"Enter the path to the QR image: \").strip()
            if not os.path.isfile(qr_file):
                print(f\"{Fore.RED}Invalid file path.\")
                continue

            output_path = input(\"Enter the path to save decoded data: \").strip()
            if not output_path:
                print(f\"{Fore.RED}No output path provided.\")
                continue

            enc_choice = input(\"Data was encrypted? (y/n): \").lower()
            comp_choice = input(\"Data was compressed? (y/n): \").lower()

            try:
                raw_data = embed_extract.decode_qr(qr_file)
                if not raw_data:
                    print(f\"{Fore.RED}No data found or error decoding QR code.\")
                    logging.warning(\"Decoded QR data is empty.\")
                    continue

                if enc_choice == 'y':
                    raw_data = crypto.decrypt(raw_data)
                    logging.info(\"QR data decrypted.\")

                if comp_choice == 'y':
                    raw_data = compressor.decompress(raw_data)
                    logging.info(\"QR data decompressed.\")

                with open(output_path, 'wb') as f:
                    f.write(raw_data)
                print(f\"{Fore.GREEN}Decoded data saved to {output_path}.\")
                logging.info(\"QR decoding successful.\")
            except Exception as e:
                print(f\"{Fore.RED}Error: {str(e)}\")
                logging.exception(\"Exception during QR decoding\")

        # 7) Exit
        elif choice == '7':
            print(f\"{Fore.CYAN}Exiting. Goodbye!\")
            sys.exit(0)

        else:
            print(f\"{Fore.RED}Invalid choice. Please try again.\")

def main():
    print_banner()
    run_menu()


if __name__ == '__main__':
    main()
