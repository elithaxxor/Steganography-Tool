# retrieve_embedded_exec.py
class RetrieveEmbeddedExec:
    @staticmethod
    def retrieve_embedded_exec(image_path, output_exec_path):
        with open(image_path, 'rb') as image_file:
            data = image_file.read()
            eoi_index = data.rfind(b'\xFF\xD9')
            if eoi_index != -1:
                embedded_data = data[eoi_index + 2:]
                with open(output_exec_path, 'wb') as output_file:
                    output_file.write(embedded_data)
