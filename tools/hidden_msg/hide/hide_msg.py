from steganography_tool import hide_message

class MessageHider:
    def __init__(self, image_path, message, output_path):
        self.image_path = image_path
        self.message = message
        self.output_path = output_path

    def hide_message(self):
        hide_message(self.image_path, self.message, self.output_path)
        print(f'Message hidden in {self.output_path}')
