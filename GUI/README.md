# 🔒 Steganography Tool+Detector v2.0 

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

- **📊 Multiple File Format Support**: Hide data within JPEG, PNG, GIF images, PDF files, WAV audio files, MP4 video files, or generate a QR code with the hidden data
- **🔍 Data Extraction**: Seamlessly retrieve hidden data from supported file formats
- **🔐 Strong Encryption**: Optionally encrypt data before embedding using Fernet symmetric encryption for enhanced security
- **📦 Data Compression**: Reduce the size of embedded data using zlib compression
- **🕵️‍♂️ Steganography Detection**: Analyze files to detect if they contain hidden data using statistical analysis
- **📊 Batch Processing**: Process multiple files at once for efficient operations
- **📈 Progress Tracking**: Visual progress bars keep you informed during time-consuming operations
- **🖥️ Intuitive GUI**: Easy-to-use interface built with PySimpleGUI for improved user experience
- **📝 Comprehensive Logging**: Detailed logging of operations for debugging and audit purposes
- **⚙️ Cross-Platform**: Works on Windows, macOS, and Linux

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

## 🕵️‍♂️ Steganography Detection

The Steganography Tool includes advanced detection capabilities to analyze files and determine if they contain hidden data. The detection system uses several statistical analysis techniques:

### Detection Methods

1. **LSB Distribution Analysis**: Examines the distribution of least significant bits in the file. In natural files, LSBs should be randomly distributed (approximately 50% 0s and 50% 1s). Steganography often alters this distribution.

2. **Color Channel Correlation**: In natural images and videos, there is usually some correlation between color channels. Steganography tends to reduce this correlation.

3. **Sample Pair Analysis**: Analyzes patterns in adjacent samples (pixels, audio samples) to detect unnatural distortions caused by data hiding.

4. **Spectral Analysis**: For audio files, examines the frequency spectrum for discontinuities that might indicate hidden data.

5. **PDF Metadata Analysis**: Checks PDF files for suspicious metadata fields or embedded objects that might contain hidden data.

### Interpretation of Results

The detector provides a probability score between 0 and 1:

- **0.0 - 0.3**: Low probability of hidden data
- **0.3 - 0.7**: Medium probability of hidden data
- **0.7 - 1.0**: High probability of hidden data

The detection system also provides detailed analysis information to help understand why a certain probability was assigned.

### Limitations

- Detection is probabilistic, not deterministic - false positives and false negatives are possible
- Very small amounts of hidden data may not be detected
- Sophisticated steganography techniques designed to evade detection may not be caught
- Detection effectiveness varies by file type and steganography method

## 🚀 Usage

### Getting Started

1. **Launch the application**:
   ```bash
   python GUI/main.py
   ```

2. **The GUI window will open with two main tabs**: `Embed` and `Extract`

 embedding
6. Optionally check **Compress Data** to compress the data before embedding
7. Click `Embed Data` to start the embedding process
8. The application will save the file with the embedded data in your selected output location

### 📤 Extracting Data

1. Select the `Extract` tab
2. Choose the **File Format** of the carrier file (JPEG, PNG, GIF, PDF, QR, WAV, MP4)
3. Select either **Single File** or **Batch Processing** mode
4. For single files:
   - Browse and select the **Carrier File** from which to extract the data
   - Specify the **Output Path** where the extracted data will be saved
5. For batch processing:
   - Browse and select the **Carrier Directory** containing files to process
   - Specify the **Output Directory** where extracted data will be saved
6. Check **Encrypted** if the data was encrypted
7. Check **Compressed** if the data was compressed
8. Click `Extract Data` to start the extraction process
9. The progress bar will display the current operation status

### 🕵️‍♂️ Detecting Steganography

1. Select the `Detect` tab
2. Browse and select the **File to Analyze**
3. Click `Detect Steganography` to start the analysis
4. The tool will analyze the file and display:
   - An overall probability that the file contains hidden data
   - An interpretation of the result (Low, Medium, or High probability)
   - Detailed analysis metrics in the details area

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

### Batch Processing

#### Batch Embed
```python
from GUI.EmbedExtract import EmbedExtract, Cryptography, Compressor
from GUI.batch_processor import BatchProcessor

# Initialize components
embed_extract = EmbedExtract()
crypto = Cryptography()
compressor = Compressor()
batch_processor = BatchProcessor(embed_extract, crypto, compressor)

# Define a progress callback function
def update_progress(completed, total):
    print(f"Progress: {completed}/{total} files processed")

batch_processor.set_progress_callback(update_progress)

# Embed the same data into multiple image files
with open('secret_data.txt', 'rb') as f:
    payload_data = f.read()

# Get all PNG files in a directory
import glob
carrier_files = glob.glob('/path/to/images/*.png')

# Process the batch with encryption and compression
results = batch_processor.process_batch_embed(
    'png',                 # File format
    carrier_files,         # List of carrier files
    payload_data,          # Data to embed
    encrypt=True,          # Enable encryption
    compress=True,         # Enable compression
    max_workers=4          # Number of parallel processes
)

# Check results
for file, success in results.items():
    print(f"{file}: {'Success' if success else 'Failed'}")
```

#### Batch Extract
```python
from GUI.EmbedExtract import EmbedExtract, Cryptography, Compressor
from GUI.batch_processor import BatchProcessor

# Initialize components
embed_extract = EmbedExtract()
crypto = Cryptography()
compressor = Compressor()
batch_processor = BatchProcessor(embed_extract, crypto, compressor)

# Define a progress callback function
def update_progress(completed, total):
    print(f"Progress: {completed}/{total} files processed")

batch_processor.set_progress_callback(update_progress)

# Get all embedded PNG files in a directory
import glob
carrier_files = glob.glob('/path/to/embedded/images/*.png')

# Extract data from all files to an output directory
results = batch_processor.process_batch_extract(
    'png',                     # File format
    carrier_files,             # List of carrier files
    '/path/to/output/dir',     # Output directory
    encrypt=True,              # Data is encrypted
    compress=True,             # Data is compressed
    max_workers=4              # Number of parallel processes
)

# Check results
for file, success in results.items():
    print(f"{file}: {'Success' if success else 'Failed'}")
```

### Steganography Detection

```python
from GUI.stego_detector import StegoDetector

# Initialize the detector
detector = StegoDetector()

# Detect steganography in an image file
probability, details, file_type, interpretation = detector.detect_file('image.png')

# Display the results
print(f"Detection Result: {probability:.2%} - {interpretation}")
print(f"File Type: {file_type}")
print("\nAnalysis Details:")
for key, value in details.items():
    if isinstance(value, float):
        print(f"- {key}: {value:.4f}")
    else:
        print(f"- {key}: {value}")
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
