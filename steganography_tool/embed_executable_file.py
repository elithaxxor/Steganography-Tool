# embed_executable_file.py
class EmbedExecutableFile:
    @staticmethod
    def embed_executable_file(image_path, exec_path):
        with open(image_path, 'ab') as image_file:
            with open(exec_path, 'rb') as exec_file:
                exec_data = exec_file.read()
                image_file.write(exec_data)
