import os
import io
import zlib
import base64
import logging
import PyPDF2
import qrcode
from PIL import Image
from cryptography.fernet import Fernet
from pyzbar.pyzbar import decode

class Cryptography:
    """Class for handling encryption and decryption of data."""
    
    def __init__(self, key=None):
        """Initialize with an optional key, or generate a new one."""
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data):
        """Encrypt binary data."""
        return self.cipher.encrypt(data)
    
    def decrypt(self, data):
        """Decrypt binary data."""
        return self.cipher.decrypt(data)
    
    def get_key(self):
        """Return the current key."""
        return self.key

class Compressor:
    """Class for handling compression and decompression of data."""
    
    def compress(self, data):
        """Compress binary data."""
        return zlib.compress(data)
    
    def decompress(self, data):
        """Decompress binary data."""
        return zlib.decompress(data)

class EmbedExtract:
    """Class for embedding and extracting data from different file formats."""
    
    def __init__(self):
        """Initialize the class with logging setup."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    # Existing methods for binary embedding/extraction (JPEG, PNG, GIF)
    def embed_binary(self, carrier_path, data, file_format):
        """Embed binary data into an image file.
        
        This is a placeholder function. Actual implementation would depend on the
        specific steganography technique used for each file format.
        """
        try:
            # Open the carrier image
            img = Image.open(carrier_path)
            
            # Convert data to bytes if it's not already
            if isinstance(data, str):
                data = data.encode()
            
            # Create a binary representation of the data length
            data_len = len(data).to_bytes(4, byteorder='big')
            
            # Combine length and data
            complete_data = data_len + data
            
            # Get the pixels of the image as a list
            pixels = list(img.getdata())
            
            # Check if the image can hold the data
            if len(complete_data) > len(pixels):
                logging.error('Data too large for carrier image')
                return False
            
            # Embed the data into the pixels
            # This is a simple implementation, actual steganography techniques 
            # would be more sophisticated
            new_pixels = []
            data_index = 0
            
            for pixel in pixels:
                if isinstance(pixel, int):  # Grayscale
                    if data_index < len(complete_data):
                        # Embed data into the least significant bit
                        new_pixel = (pixel & 0xFE) | ((complete_data[data_index] & 0x80) >> 7)
                        new_pixels.append(new_pixel)
                        data_index += 1
                    else:
                        new_pixels.append(pixel)
                else:  # RGB or RGBA
                    if data_index < len(complete_data):
                        r, g, b = pixel[0:3]
                        # Embed data into the least significant bit of red channel
                        r = (r & 0xFE) | ((complete_data[data_index] & 0x80) >> 7)
                        
                        if len(pixel) == 4:  # RGBA
                            new_pixels.append((r, g, b, pixel[3]))
                        else:  # RGB
                            new_pixels.append((r, g, b))
                        
                        data_index += 1
                    else:
                        new_pixels.append(pixel)
            
            # Create a new image with the modified pixels
            new_img = Image.new(img.mode, img.size)
            new_img.putdata(new_pixels)
            
            # Save the new image, overwriting the original
            output_path = os.path.splitext(carrier_path)[0] + "_embedded." + file_format
            new_img.save(output_path)
            
            logging.info(f'Data embedded successfully into {output_path}')
            return True
        
        except Exception as e:
            logging.exception(f'Error embedding data: {str(e)}')
            return False
    
    def extract_binary(self, carrier_path, file_format):
        """Extract binary data from an image file.
        
        This is a placeholder function. Actual implementation would depend on the
        specific steganography technique used for each file format.
        """
        try:
            # Open the carrier image
            img = Image.open(carrier_path)
            
            # Get the pixels of the image as a list
            pixels = list(img.getdata())
            
            # Extract the data length (first 4 bytes)
            data_len_bytes = bytearray(4)
            data_index = 0
            
            for pixel in pixels[:32]:  # 32 pixels for 4 bytes (8 bits per byte)
                if isinstance(pixel, int):  # Grayscale
                    # Extract the least significant bit
                    bit = pixel & 0x01
                    byte_index = data_index // 8
                    bit_index = 7 - (data_index % 8)
                    
                    if bit:
                        data_len_bytes[byte_index] |= (1 << bit_index)
                    
                    data_index += 1
                else:  # RGB or RGBA
                    # Extract the least significant bit from the red channel
                    bit = pixel[0] & 0x01
                    byte_index = data_index // 8
                    bit_index = 7 - (data_index % 8)
                    
                    if bit:
                        data_len_bytes[byte_index] |= (1 << bit_index)
                    
                    data_index += 1
            
            # Convert the bytes to an integer
            data_len = int.from_bytes(data_len_bytes, byteorder='big')
            
            # Extract the actual data
            data_bytes = bytearray(data_len)
            data_index = 0
            
            for pixel in pixels[32:32 + data_len * 8]:  # Skip the length bytes
                if isinstance(pixel, int):  # Grayscale
                    # Extract the least significant bit
                    bit = pixel & 0x01
                    byte_index = data_index // 8
                    bit_index = 7 - (data_index % 8)
                    
                    if bit:
                        data_bytes[byte_index] |= (1 << bit_index)
                    
                    data_index += 1
                    if data_index >= data_len * 8:
                        break
                else:  # RGB or RGBA
                    # Extract the least significant bit from the red channel
                    bit = pixel[0] & 0x01
                    byte_index = data_index // 8
                    bit_index = 7 - (data_index % 8)
                    
                    if bit:
                        data_bytes[byte_index] |= (1 << bit_index)
                    
                    data_index += 1
                    if data_index >= data_len * 8:
                        break
            
            logging.info(f'Data extracted successfully from {carrier_path}')
            return bytes(data_bytes)
        
        except Exception as e:
            logging.exception(f'Error extracting data: {str(e)}')
            return None
    
    # New method for PDF embedding
    def embed_pdf(self, carrier_path, data):
        """Embed binary data into a PDF file."""
        try:
            # Read the PDF file
            with open(carrier_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Copy all pages from the original PDF
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)
                
                # Encode the data as base64 to ensure it's valid for a text string
                encoded_data = base64.b64encode(data).decode('utf-8')
                
                # Add the data as a hidden document-level metadata
                pdf_writer.add_metadata({
                    '/StegData': encoded_data
                })
                
                # Get the output path
                output_path = os.path.splitext(carrier_path)[0] + "_embedded.pdf"
                
                # Write the output PDF
                with open(output_path, 'wb') as out_file:
                    pdf_writer.write(out_file)
            
            logging.info(f'Data embedded successfully into {output_path}')
            return True
        
        except Exception as e:
            logging.exception(f'Error embedding data in PDF: {str(e)}')
            return False
    
    # New method for PDF extraction
    def extract_pdf(self, carrier_path):
        """Extract binary data from a PDF file."""
        try:
            # Read the PDF file
            with open(carrier_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                
                # Extract the metadata containing the steganographic data
                if '/StegData' in pdf_reader.metadata:
                    encoded_data = pdf_reader.metadata['/StegData']
                    
                    # Decode the base64 data
                    data = base64.b64decode(encoded_data)
                    
                    logging.info(f'Data extracted successfully from {carrier_path}')
                    return data
                else:
                    logging.error('No steganographic data found in the PDF')
                    return None
        
        except Exception as e:
            logging.exception(f'Error extracting data from PDF: {str(e)}')
            return None
    
    # New method for QR code embedding
    def embed_qr(self, data, output_path):
        """Embed binary data into a QR code and save as an image."""
        try:
            # Encode the data as base64 to ensure it's valid for a QR code
            encoded_data = base64.b64encode(data).decode('utf-8')
            
            # Create the QR code
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            
            # Add the data to the QR code
            qr.add_data(encoded_data)
            qr.make(fit=True)
            
            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save the QR code image
            img.save(output_path)
            
            logging.info(f'QR code with embedded data saved to {output_path}')
            return True
        
        except Exception as e:
            logging.exception(f'Error creating QR code: {str(e)}')
            return False
    
    # New method for QR code extraction
    def extract_qr(self, carrier_path):
        """Extract binary data from a QR code image."""
        try:
            # Open the QR code image
            img = Image.open(carrier_path)
            
            # Decode the QR code
            decoded = decode(img)
            
            if not decoded:
                logging.error('No QR code found in the image')
                return None
            
            # Get the decoded data
            encoded_data = decoded[0].data.decode('utf-8')
            
            # Decode the base64 data
            data = base64.b64decode(encoded_data)
            
            logging.info(f'Data extracted successfully from QR code {carrier_path}')
            return data
        
        except Exception as e:
            logging.exception(f'Error extracting data from QR code: {str(e)}')
            return None
