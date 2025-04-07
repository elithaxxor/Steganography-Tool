# 🔒 Steganography Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)
![Stars](https://img.shields.io/github/stars/elithaxxor/Steganography-Tool?style=social)

<p align="center">
  <img src="https://i.imgur.com/P4oGIBv.png" width="200" alt="Steganography Logo">
</p>

<p align="center">
  <b>Hide data in plain sight with advanced steganography techniques</b>
</p>

## 📖 Overview

The Steganography Tool provides a powerful yet user-friendly graphical interface for embedding and extracting data within various file formats using advanced steganography techniques. This tool enables you to hide sensitive information within ordinary-looking files, making it invisible to casual observers. With additional features like encryption and compression, your hidden data remains secure and efficient.

## ✨ Features

- **📊 Multiple File Format Support**: Hide data within JPEG, PNG, GIF images, PDF files, or generate a QR code with the hidden data
- **🔍 Data Extraction**: Seamlessly retrieve hidden data from supported file formats
- **🔐 Strong Encryption**: Optionally encrypt data before embedding using Fernet symmetric encryption for enhanced security
- **📦 Data Compression**: Reduce the size of embedded data using zlib compression
- **🖥️ Intuitive GUI**: Easy-to-use interface built with PySimpleGUI for improved user experience
- **📝 Comprehensive Logging**: Detailed logging of operations for debugging and audit purposes
- **⚙️ Cross-Platform**: Works on Windows, macOS, and Linux

## 🛠️ Installation

### Prerequisites

- Python 3.6 or higher
- Git (for cloning the repository)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/elithaxxor/Steganography-Tool.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Steganography-Tool
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📚 Dependencies

The tool relies on the following Python packages:
- `PySimpleGUI` - For the graphical user interface
- `Pillow` - For image processing
- `PyPDF2` - For PDF manipulation
- `qrcode` - For QR code generation
- `pyzbar` - For QR code reading
- `cryptography` - For encryption and decryption
- Standard libraries: `os`, `io`, `zlib`, `base64`, `logging`

## 🚀 Usage

### Getting Started

1. **Launch the application**:
   ```bash
   python GUI/main.py
   ```

2. **The GUI window will open with two main tabs**: `Embed` and `Extract`

### 📥 Embedding Data

1. Select the `Embed` tab
2. Choose the **File Format** of the carrier file (JPEG, PNG, GIF, PDF, QR)
3. Browse and select the **Carrier File** in which to hide the data
4. Browse and select the **Payload File** containing the data to be hidden
5. Optionally check **Encrypt Data** to encrypt the data before embedding
6. Optionally check **Compress Data** to compress the data before embedding
7. Click `Embed Data` to start the embedding process
8. The application will save the file with the embedded data in your selected output location

### 📤 Extracting Data

1. Select the `Extract` tab
2. Choose the **File Format** of the carrier file (JPEG, PNG, GIF, PDF, QR)
3. Browse and select the **Carrier File** from which to extract the data
4. Specify the **Output Path** where the extracted data will be saved
5. Check **Encrypted** if the data was encrypted
6. Check **Compressed** if the data was compressed
7. Click `Extract Data` to start the extraction process
8. The extracted data will be saved to your specified output path

## 💻 Code Examples

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

## 📸 Screenshots

<p align="center">
  <img src="screenshots/embed_tab.png" width="48%" alt="Embed Tab">
  <img src="screenshots/extract_tab.png" width="48%" alt="Extract Tab">
</p>

## 🔍 How It Works

The Steganography Tool uses different techniques depending on the file format:

- **Images (PNG, JPEG, GIF)**: Uses the least significant bits (LSB) of pixel values to store hidden data
- **PDF**: Embeds data within PDF metadata or document objects
- **QR Code**: Generates a QR code that contains the encoded data

When encryption is enabled, the data is encrypted using Fernet symmetric encryption with a secure key before embedding. When compression is enabled, zlib compression is applied to reduce the size of the data.

## 🛣️ Roadmap

Future enhancements planned for the Steganography Tool:

- **Audio File Support**: Add the ability to hide data in WAV and MP3 files
- **Video File Support**: Implement steganography techniques for video files
- **Batch Processing**: Enable processing multiple files at once
- **Advanced Encryption Options**: Add more encryption algorithms and options
- **Custom File Headers**: Allow users to create custom file headers for improved stealth
- **Watermarking**: Add digital watermarking capabilities

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the Steganography Tool, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for detailed information.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) - For the GUI framework
- [Pillow](https://python-pillow.org/) - For image manipulation
- [PyPDF2](https://github.com/mstamy2/PyPDF2) - For PDF manipulation
- [QRCode](https://github.com/lincolnloop/python-qrcode) - For QR code generation
- [Pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) - For QR code reading

## 📬 Contact

If you have any questions or feedback, feel free to reach out to the project maintainer at [maintainer@example.com](mailto:maintainer@example.com).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/elithaxxor">elithaxxor</a>
</p>
