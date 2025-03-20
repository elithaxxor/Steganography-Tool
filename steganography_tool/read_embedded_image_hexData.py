# read_embedded_image_hexData.py
from io import BytesIO
from PIL import Image

class ReadEmbeddedImageHexData:
    @staticmethod
    def read_embedded_image_hexData(image_path):
        with open(image_path, 'rb') as image_file:
            data = image_file.read()
            eoi_index = data.rfind(b'\xFF\xD9')
            if eoi_index != -1:
                embedded_data = data[eoi_index + 2:]
                return Image.open(BytesIO(embedded_data))
        return None
