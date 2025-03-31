#!/usr/bin/env python3
import os
import platform
import psutil

import zlib
import traceback
from cryptography.fernet import Fernet

from PIL import Image
import qrcode
from pyzbar.pyzbar import decode
from PyPDF2 import PdfReader, PdfWriter

from colorama import Fore, Style, init

init(autoreset=True)

#########################################
#         SYSTEM INFORMATION            #
#########################################

def display_system_info():
    print(f\"{Fore.CYAN}System Information:\")
    print(f\"{Fore.GREEN}OS: {platform.system()} {platform.release()}\")
    print(f\"{Fore.GREEN}Processor: {platform.processor()}\")
    print(f\"{Fore.GREEN}Architecture: {platform.architecture()[0]}\")
    print(f\"{Fore.GREEN}Machine: {platform.machine()}\")
    print(f\"{Fore.GREEN}Python Version: {platform.python_version()}\")
    
    print(f\"\\n{Fore.CYAN}Disk Information:\")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f\"{Fore.GREEN}Device: {partition.device}\")
        print(f\"{Fore.GREEN}Mountpoint: {partition.mountpoint}\")
        print(f\"{Fore.GREEN}File system type: {partition.fstype}\")
        usage = psutil.disk_usage(partition.mountpoint)
        print(f\"{Fore.GREEN}Total Size: {usage.total / (1024 ** 3):.2f} GB\")
        print(f\"{Fore.GREEN}Used: {usage.used / (1024 ** 3):.2f} GB\")
        print(f\"{Fore.GREEN}Free: {usage.free / (1024 ** 3):.2f} GB\")
        print(f\"{Fore.GREEN}Percentage: {usage.percent}%\\n\")

#########################################
#         CLASSES & STEGO LOGIC         #
#########################################

class MessageHider:
    \"\"\"
    Basic text-in-image hiding logic (dummy example).
    In reality, you might manipulate pixels to store text bits, or use LSB, etc.
    \"\"\"
    def __init__(self, image_path, message, output_path):
        self.image_path = image_path
        self.message = message
        self.output_path = output_path

    def hide_message(self):
        # For demonstration, we simply append text to the end of the file.
        # Real steganography modifies pixel data or uses robust algorithms.
        try:
            with open(self.image_path, 'rb') as orig_img:
                img_data = orig_img.read()
            with open(self.output_path, 'wb') as out_img:
                out_img.write(img_data)
                out_img.write(b'--HIDDEN-TEXT--')
                out_img.write(self.message.encode('utf-8'))
            print(f\"{Fore.GREEN}Message hidden successfully in {self.output_path}.\")
        except Exception as e:
            print(f\"{Fore.RED}Error hiding message: {e}\")
            traceback.print_exc()

class MessageReceiver:
    \"\"\"
    Basic text retrieval from image end-of-file for demonstration.
    \"\"\"
    def __init__(self, image_path):
        self.image_path = image_path

    def retrieve_message(self):
        try:
            with open(self.image_path, 'rb') as img:
                content = img.read()
            marker = b'--HIDDEN-TEXT--'
            idx = content.find(marker)
            if idx == -1:
                print(f\"{Fore.RED}No hidden message found.\")
                return
            hidden_part = content[idx + len(marker):]
            message = hidden_part.decode('utf-8', errors='replace')
            print(f\"{Fore.GREEN}Hidden message: {message}\")
        except Exception as e:
            print(f\"{Fore.RED}Error retrieving message: {e}\")
            traceback.print_exc()

class BinaryStego:
    \"\"\"
    Embed or extract binary data in:
      - JPEG/PNG/GIF (appending after EOF marker),
      - PDF (metadata),
      - QR codes (embedding as text).
    For real stego, you'd do more advanced manipulations.
    \"\"\"
    # Common EOF markers
    EOF_MARKERS = {
        'jpeg': b'\\xff\\xd9',
        'png': b'IEND\\xaeB`\\x82',
        'gif': b'\\x00;',
    }

    def __init__(self, carrier_path=None, second_image_path=None, payload_path=None):
        self.carrier_path = carrier_path
        self.second_image_path = second_image_path
        self.payload_path = payload_path

    # ---------- Basic embed/extract for images (JPEG/PNG/GIF) ----------
    def embed_data_in_image(self, image_path, data, fmt='jpeg'):
        \"\"\"Append data after file EOF marker.\"\"\"
        marker = self.EOF_MARKERS.get(fmt, None)
        if not marker:
            raise ValueError(\"Unsupported format: \" + fmt)

        try:
            with open(image_path, 'ab') as f:
                f.write(marker)        # re-insert marker
                f.write(data)          # embed your payload
            print(f\"{Fore.GREEN}Data successfully appended to {image_path}.\")
        except Exception as e:
            print(f\"{Fore.RED}Error embedding data in image: {e}\")
            traceback.print_exc()

    def extract_data_from_image(self, image_path, fmt='jpeg'):
        \"\"\"Find data after file EOF marker.\"\"\"
        marker = self.EOF_MARKERS.get(fmt, None)
        if not marker:
            raise ValueError(\"Unsupported format: \" + fmt)

        try:
            with open(image_path, 'rb') as f:
                content = f.read()
            idx = content.find(marker)
            if idx == -1:
                print(f\"{Fore.RED}No embedded data found.\")
                return None
            embedded_data = content[idx + len(marker):]
            print(f\"{Fore.GREEN}Data extracted from image.\")
            return embedded_data
        except Exception as e:
            print(f\"{Fore.RED}Error extracting data from image: {e}\")
            traceback.print_exc()
            return None

    # ---------- PDF-based metadata ----------
    def embed_data_in_pdf(self, pdf_path, data):
        \"\"\"Store data as text in PDF metadata /HiddenData.\"\"\"
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            text_data = data.decode('utf-8', errors='replace')
            writer.add_metadata({\"/HiddenData\": text_data})

            base = os.path.basename(pdf_path)
            new_pdf = f\"embedded_{base}\"
            with open(new_pdf, 'wb') as out_pdf:
                writer.write(out_pdf)

            print(f\"{Fore.GREEN}Data embedded in PDF metadata -> {new_pdf}\")
        except Exception as e:
            print(f\"{Fore.RED}Error embedding data in PDF: {e}\")
            traceback.print_exc()

    def extract_data_from_pdf(self, pdf_path):
        \"\"\"Extract data from PDF metadata /HiddenData.\"\"\"
        try:
            reader = PdfReader(pdf_path)
            meta = reader.metadata
            if \"/HiddenData\" not in meta:
                print(f\"{Fore.RED}No hidden data in PDF metadata.\")
                return None
            hidden_text = meta.get(\"/HiddenData\")
            if not hidden_text:
                print(f\"{Fore.RED}No hidden data found.\")
                return None
            print(f\"{Fore.GREEN}Data extracted from PDF metadata.\")
            return hidden_text.encode('utf-8')
        except Exception as e:
            print(f\"{Fore.RED}Error extracting data from PDF: {e}\")
            traceback.print_exc()
            return None

    # ---------- QR-based embedding & extracting ----------
    def create_qr(self, data, output_file):
        \"\"\"Embed binary data as text in a QR code.\"\"\"
        try:
            text_data = data.decode('utf-8', errors='replace')
            qr_img = qrcode.make(text_data)
            qr_img.save(output_file)
            print(f\"{Fore.GREEN}QR code created -> {output_file}\")
        except Exception as e:
            print(f\"{Fore.RED}Error creating QR code: {e}\")
            traceback.print_exc()

    def decode_qr(self, qr_image_path):
        \"\"\"Read a QR code and return raw bytes.\"\"\"
        try:
            img = Image.open(qr_image_path)
            decoded_info = decode(img)
            if not decoded_info:
                print(f\"{Fore.RED}No QR data found.\")
                return None
            print(f\"{Fore.GREEN}QR code decoded.\")
            return decoded_info[0].data
        except Exception as e:
            print(f\"{Fore.RED}Error decoding QR code: {e}\")
            traceback.print_exc()
            return None

#########################################
#         MAIN MENU & WORKFLOW          #
#########################################

def main_menu():
    \"\"\"A single menu that demonstrates text stego (MessageHider/MessageReceiver) and binary stego (BinaryStego).\"\"\"
    stego = BinaryStego()  # We'll reuse this instance for embedding/extracting
    while True:
        print(f\"{Fore.CYAN}\\nMain Menu:\")
        print(f\"{Fore.YELLOW}1. Hide a message in an image (text stego)\")
        print(f\"{Fore.YELLOW}2. Retrieve a hidden message from an image (text stego)\")
        print(f\"{Fore.YELLOW}3. Embed binary data in an image (JPEG, PNG, GIF)\")
        print(f\"{Fore.YELLOW}4. Extract binary data from an image (JPEG, PNG, GIF)\")
        print(f\"{Fore.YELLOW}5. Embed binary data in PDF (metadata)\")
        print(f\"{Fore.YELLOW}6. Extract binary data from PDF (metadata)\")
        print(f\"{Fore.YELLOW}7. Create QR code from binary data\")
        print(f\"{Fore.YELLOW}8. Decode QR code to retrieve binary data\")
        print(f\"{Fore.RED}9. Exit\")

        choice = input(f\"{Fore.CYAN}Enter your choice: \").strip()

        if choice == '1':
            image_path = input(f\"{Fore.CYAN}Enter the path to the image: \").strip()
            message = input(f\"{Fore.CYAN}Enter the message to hide: \").strip()
            output_path = input(f\"{Fore.CYAN}Enter the output path for the image: \").strip()
            hider = MessageHider(image_path, message, output_path)
            hider.hide_message()

        elif choice == '2':
            image_path = input(f\"{Fore.CYAN}Enter the path to the image: \").strip()
            receiver = MessageReceiver(image_path)
            receiver.retrieve_message()

        elif choice == '3':
            img_path = input(f\"{Fore.CYAN}Enter the path to the carrier image (JPEG/PNG/GIF): \").strip()
            fmt = input(f\"{Fore.CYAN}Enter format (jpeg/png/gif): \").lower().strip()
            data_path = input(f\"{Fore.CYAN}Enter the path to the binary payload: \").strip()

            if not os.path.isfile(img_path):
                print(f\"{Fore.RED}Invalid carrier file.\")
                continue
            if not os.path.isfile(data_path):
                print(f\"{Fore.RED}Invalid payload file.\")
                continue

            with open(data_path, 'rb') as f:
                payload_data = f.read()
            stego.embed_data_in_image(img_path, payload_data, fmt)

        elif choice == '4':
            img_path = input(f\"{Fore.CYAN}Enter the path to the carrier image (JPEG/PNG/GIF): \").strip()
            fmt = input(f\"{Fore.CYAN}Enter format (jpeg/png/gif): \").lower().strip()
            output_file = input(f\"{Fore.CYAN}Enter the output file to save extracted data: \").strip()
            
            extracted = stego.extract_data_from_image(img_path, fmt)
            if extracted:
                with open(output_file, 'wb') as out:
                    out.write(extracted)

        elif choice == '5':
            pdf_path = input(f\"{Fore.CYAN}Enter the path to the PDF: \").strip()
            data_path = input(f\"{Fore.CYAN}Enter the path to the binary data to embed: \").strip()
            if not os.path.isfile(pdf_path):
                print(f\"{Fore.RED}Invalid PDF file.\")
                continue
            if not os.path.isfile(data_path):
                print(f\"{Fore.RED}Invalid data file.\")
                continue

            with open(data_path, 'rb') as f:
                pdf_payload = f.read()
            stego.embed_data_in_pdf(pdf_path, pdf_payload)

        elif choice == '6':
            pdf_path = input(f\"{Fore.CYAN}Enter the path to the PDF: \").strip()
            output_file = input(f\"{Fore.CYAN}Enter the output file to save extracted data: \").strip()
            extracted = stego.extract_data_from_pdf(pdf_path)
            if extracted:
                with open(output_file, 'wb') as out:
                    out.write(extracted)

        elif choice == '7':
            data_path = input(f\"{Fore.CYAN}Enter the path to the binary data for the QR code: \").strip()
            output_file = input(f\"{Fore.CYAN}Enter output filename for the QR code (e.g. code.png): \").strip()
            if not os.path.isfile(data_path):
                print(f\"{Fore.RED}Invalid data path.\")
                continue

            with open(data_path, 'rb') as f:
                qr_data = f.read()
            stego.create_qr(qr_data, output_file)

        elif choice == '8':
            qr_file = input(f\"{Fore.CYAN}Enter the path to the QR code image: \").strip()
            if not os.path.isfile(qr_file):
                print(f\"{Fore.RED}Invalid QR file.\")
                continue

            output_file = input(f\"{Fore.CYAN}Enter output file for decoded data: \").strip()
            decoded = stego.decode_qr(qr_file)
            if decoded:
                with open(output_file, 'wb') as out:
                    out.write(decoded)

        elif choice == '9':
            print(f\"{Fore.RED}Exiting...\")
            break
        else:
            print(f\"{Fore.RED}Invalid choice. Please try again.\")

#########################################
#                 MAIN                  #
#########################################

if __name__ == '__main__':
    display_system_info()
    main_menu()
