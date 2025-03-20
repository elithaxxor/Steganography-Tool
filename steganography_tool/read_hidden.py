# read_hidden.py
def read_hidden(image_path):
    with open(image_path, 'rb') as image_file:
        data = image_file.read()
        eoi_index = data.rfind(b'\xFF\xD9')
        if eoi_index != -1:
            return data[eoi_index + 2:]
    return b''
