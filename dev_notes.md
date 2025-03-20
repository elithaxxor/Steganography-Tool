JPEG Steganography Code Analysis
Identified Functions

add_text: Appends text to an image file

Bug identified: Code uses literal bytes string b'input_text' instead of converting the variable input_text to bytes


read_hidden: Extracts data appended after JPEG's EOI marker (FFD9)

Finds FFD9 index, seeks to OFFSET+2, reads appended data


embed_image_hexData: Embeds a PNG image after JPEG's EOI marker

Converts second image to PNG format
Saves to BytesIO buffer
Appends PNG data after original JPEG's FFD9 marker


read_embedded_image_hexData: Extracts embedded PNG image

Locates FFD9 marker
Seeks past it
Uses PIL to read PNG data from bytes stream


embed_executable_file: Appends executable file contents after image

Simply appends binary data to original image


retrieve_embedded_exec: Extracts embedded executable

Finds FFD9
Seeks past it
Writes remaining data to new executable file
