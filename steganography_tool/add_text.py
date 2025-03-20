# add_text.py
def add_text(image_path, text):
    with open(image_path, 'ab') as image_file:
        image_file.write(text.encode('utf-8'))

# Bug fix: Ensure 'text' is converted to bytes
# Original code used: b'input_text'
# Refactored code correctly converts 'input_text' to bytes 03/16
