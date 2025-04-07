# 🔒 Steganography Tool v1.4

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Version](https://img.shields.io/badge/version-1.1.0-orange.svg)
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

- **📊 Multiple File Format Support**: Hide data within JPEG, PNG, GIF images, PDF files, WAV audio files, MP4 video files

## 🔬 How LSB Steganography Works

Least Significant Bit (LSB) steganography is the primary technique used in this tool for embedding data in images, audio, and video files. Here's how it works:

### Basic Principle

Digital media files (images, audio, video) store data as a sequence of bytes. Each byte consists of 8 bits. In LSB steganography, we replace the least significant bit (the rightmost bit) of each byte with a bit from our secret data. Since this bit has the smallest impact on the value, changing it creates only a minimal, often imperceptible change to the original file.

### For Different Media Types:

1. **Images**: Each pixel in an image is represented by color values (RGB or grayscale). We modify the least significant bit of these color values to store our hidden data. For example, in an RGB image, each pixel has three color values, giving us three bits per pixel that can be modified.

2. **Audio**: Audio files consist of samples that represent the amplitude of sound waves at specific time intervals. We modify the least significant bit of each sample to embed our data. Due to the limitations of human hearing, these small changes are typically inaudible.

3. **Video**: Video files are essentially sequences of images (frames) with associated audio. We can apply the same LSB technique to either the video frames, the audio track, or both.

### The Process:

1. **Embedding**:
   - Convert the secret data into a bit stream
   - For each bit of secret data, replace the LSB of a byte in the carrier file
   - The first few bytes are typically used to store the length of the hidden data

2. **Extraction**:
   - Read the LSBs from the carrier file
   - The first few bits indicate the length of the hidden message
   - Continue extracting LSBs until the complete message is retrieved

### Advantages:

- Minimal visual/auditory impact on the carrier file
- Relatively simple to implement
- Difficult to detect without special analysis tools
- Large capacity compared to other steganography methods

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
- `numpy` - For numerical operations
- `opencv-python` - For video processing
- `wave` - For audio file processing
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
2. Choose the **File Format** of the carrier file (JPEG, PNG, GIF, PDF, QR, WAV, MP4)
3. Browse and select the **Carrier File** in which to hide the data
4. Browse and select the **Payload File** containing the data to be hidden
5. Optionally check **Encrypt Data** to encrypt the data before embedding
6. Optionally check **Compress Data** to compress the data before embedding
7. Click `Embed Data` to start the embedding process
8. The application will save the file with the embedded data in your selected output location

### 📤 Extracting Data

1. Select the `Extract` tab
2. Choose the **File Format** of the carrier file (JPEG, PNG, GIF, PDF, QR, WAV, MP4)
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

### Audio Steganography

#### Embed Data into an Audio File
```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Embed data into a WAV file
success = embed_extract.embed_audio('audio.wav', b'secret data')
if success:
    print("Data embedded successfully.")
```

#### Extract Data from an Audio File
```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Extract data from the embedded WAV file
extracted_data = embed_extract.extract_audio('audio_embedded.wav')
if extracted_data:
    print("Data extracted:", extracted_data)
```

### Video Steganography

#### Embed Data into a Video File
```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Embed data into an MP4 file
success = embed_extract.embed_video('video.mp4', b'secret data')
if success:
    print("Data embedded successfully.")
```

#### Extract Data from a Video File
```python
from GUI.EmbedExtract import EmbedExtract

embed_extract = EmbedExtract()

# Extract data from the embedded MP4 file
extracted_data = embed_extract.extract_video('video_embedded.mp4')
if extracted_data:
    print("Data extracted:", extracted_data)
```

## 📸 Screenshots

<p align="center">
  <img src="screenshots/embed_tab.png" width="48%" alt="Embed Tab">
  <img src="screenshots/extract_tab.png" width="48%" alt="Extract Tab">
</p>

## 🛣️ Roadmap

Future enhancements planned for the Steganography Tool:

- **Enhanced Audio Support**: Add support for MP3 and other audio formats
- **Advanced Video Options**: Configure which frames to use for embedding
- **Multiple Carrier Support**: Split large payloads across multiple carrier files
- **Advanced Encryption Options**: Add more encryption algorithms and options
- **Batch Processing**: Enable processing multiple files at once
- **Custom File Headers**: Allow users to create custom file headers for improved stealth
- **Watermarking**: Add digital watermarking capabilities
- **Steganography Detection**: Add capability to detect if a file contains hidden data
- **Password Protection**: Add password protection for encrypted data

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
- [OpenCV](https://opencv.org/) - For video processing
- [NumPy](https://numpy.org/) - For numerical operations

## 📬 Contact

If you have any questions or feedback, feel free to reach out to the project maintainer at [maintainer@example.com](mailto:maintainer@example.com).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/elithaxxor">elithaxxor</a>
</p>
