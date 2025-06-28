Identified Functions (removed in cleanup):

- add_text: Append text to an image file
- read_hidden: Extract data appended after JPEG's EOI marker (FFD9)
- embed_image_hexData: Embed a PNG image after JPEG's EOI marker
- read_embedded_image_hexData: Extract an embedded PNG image
- embed_executable_file: Append an executable file after an image
- retrieve_embedded_exec: Extract an embedded executable

These proof-of-concept helpers were replaced by the more complete
implementation found in `main.py` and the `stego_plugins` package.
