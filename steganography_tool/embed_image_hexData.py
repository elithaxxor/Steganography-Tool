# embed_image_hexData.py
from io import BytesIO
from PIL import Image

class EmbedImageHexData:
    @staticmethod
    def embed_image_hexData(jpeg_path, png_path):
        with open(jpeg_path, 'ab') as jpeg_file:
            with open(png_path, 'rb') as png_file:
                png_data = png_file.read()
                jpeg_file.write(png_data)
