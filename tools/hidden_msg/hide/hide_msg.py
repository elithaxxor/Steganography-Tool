from steganography_tool import recv_msg

image_path = 'path/to/output_image.png'

message = retrieve_message(image_path)
print(f'The hidden message is: {message}')
