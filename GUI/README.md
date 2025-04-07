# Steganography Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

The Steganography Tool provides a graphical user interface (GUI) for embedding and extracting data within various file formats using steganography techniques. It supports encryption and compression of data to ensure security and efficiency.

## Features

- **Embed Data**: Hide data within JPEG, PNG, GIF images, PDF files, or generate a QR code with the hidden data.
- **Extract Data**: Retrieve hidden data from the supported file formats.
- **Encryption**: Optionally encrypt data before embedding to enhance security.
- **Compression**: Optionally compress data before embedding to save space.
- **User-Friendly GUI**: Easy-to-use interface built with PySimpleGUI.

## Installation

### Prerequisites

- Python 3.6 or higher

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/elithaxxor/Steganography-Tool.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Steganography-Tool
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main GUI script:
    ```bash
    python GUI/main.py
    ```

2. The GUI window will open with two main tabs: `Embed` and `Extract`.

### Embed Data

- **File Format**: Select the format of the carrier file (JPEG, PNG, GIF, PDF, QR).
- **Carrier File**: Browse and select the file in which to hide the data.
- **Payload File**: Browse and select the file containing the data to be hidden.
- **Optional Encryption**: Check the box to encrypt the data before embedding.
- **Optional Compression**: Check the box to compress the data before embedding.
- Click `Embed Data` to start the embedding process.

### Extract Data

- **File Format**: Select the format of the carrier file (JPEG, PNG, GIF, PDF, QR).
- **Carrier File**: Browse and select the file from which to extract the data.
- **Output Path**: Specify the path where the extracted data will be saved.
- **Encrypted**: Check the box if the data was encrypted.
- **Compressed**: Check the box if the data was compressed.
- Click `Extract Data` to start the extraction process.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to reach out to the project maintainer at [maintainer@example.com](mailto:maintainer@example.com).

## Screenshots

![Embed Tab](screenshots/embed_tab.png)
*Embed Tab*

![Extract Tab](screenshots/extract_tab.png)
*Extract Tab*
# Steganography Tool

This repository provides a steganography tool that allows users to embed and extract data into/from various file formats, including images (JPEG, PNG, GIF), PDFs, and QR codes. The tool also supports encryption and compression of data for enhanced security and efficiency.

## Features

- **Image Steganography**: Embed and extract data into/from image files (JPEG, PNG, GIF).
- **PDF Steganography**: Embed and extract data into/from PDF files.
- **QR Code Steganography**: Embed and extract data into/from QR code images.
- **Encryption**: Encrypt and decrypt data using the Fernet symmetric encryption.
- **Compression**: Compress and decompress data using zlib.

## Requirements

- Python 3.x
- Required Python packages:
  - `os`
  - `io`
  - `zlib`
  - `base64`
  - `logging`
  - `PyPDF2`
  - `qrcode`
  - `PIL` (Pillow)
  - `cryptography`
  - `pyzbar`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/elithaxxor/Steganography-Tool.git
   cd Steganography-Tool

Sure! Here is a `MARKDOWN.md` file that includes more usage examples:

```markdown
# Steganography Tool

This repository provides a steganography tool that allows users to embed and extract data into/from various file formats, including images (JPEG, PNG, GIF), PDFs, and QR codes. The tool also supports encryption and compression of data for enhanced security and efficiency.

## Features

- **Image Steganography**: Embed and extract data into/from image files (JPEG, PNG, GIF).
- **PDF Steganography**: Embed and extract data into/from PDF files.
- **QR Code Steganography**: Embed and extract data into/from QR code images.
- **Encryption**: Encrypt and decrypt data using the Fernet symmetric encryption.
- **Compression**: Compress and decompress data using zlib.

## Requirements

- Python 3.x
- Required Python packages:
  - `os`
  - `io`
  - `zlib`
  - `base64`
  - `logging`
  - `PyPDF2`
  - `qrcode`
  - `PIL` (Pillow)
  - `cryptography`
  - `pyzbar`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/elithaxxor/Steganography-Tool.git
   cd Steganography-Tool
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Image Steganography

#### Embed Data into an Image

```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Embed data into a PNG image
success = embed_extract.embed_binary('image.png', b'secret data', 'png')
if success:
    print("Data embedded successfully.")
```

#### Extract Data from an Image

```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Extract data from the embedded PNG image
extracted_data = embed_extract.extract_binary('image_embedded.png', 'png')
if extracted_data:
    print("Data extracted:", extracted_data)
```

### PDF Steganography

#### Embed Data into a PDF

```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Embed data into a PDF file
success = embed_extract.embed_pdf('document.pdf', b'secret data')
if success:
    print("Data embedded successfully.")
```

#### Extract Data from a PDF

```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Extract data from the embedded PDF file
extracted_data = embed_extract.extract_pdf('document_embedded.pdf')
if extracted_data:
    print("Data extracted:", extracted_data)
```

### QR Code Steganography

#### Embed Data into a QR Code

```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Embed data into a QR code image
success = embed_extract.embed_qr(b'secret data', 'qrcode.png')
if success:
    print("QR code created successfully.")
```

#### Extract Data from a QR Code

```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Extract data from the QR code image
extracted_data = embed_extract.extract_qr('qrcode.png')
if extracted_data:
    print("Data extracted:", extracted_data)
```

### Encryption and Compression

#### Encrypt and Decrypt Data

```python
from GUI.EmbedExtract import Cryptography

crypto = Cryptography()

# Encrypt data
encrypted_data = crypto.encrypt(b'secret data')
print("Encrypted data:", encrypted_data)

# Decrypt data
decrypted_data = crypto.decrypt(encrypted_data)
print("Decrypted data:", decrypted_data)
```

#### Compress and Decompress Data

```python
from GUI.EmbedExtract import Compressor

compressor = Compressor()

# Compress data
compressed_data = compressor.compress(b'secret data')
print("Compressed data:", compressed_data)

# Decompress data
decompressed_data = compressor.decompress(compressed_data)
print("Decompressed data:", decompressed_data)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Created by [elithaxxor](https://github.com/elithaxxor).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## Contact

For any inquiries, please contact [elithaxxor](https://github.com/elithaxxor).

```

Feel free to add this `MARKDOWN.md` file to your repository.
