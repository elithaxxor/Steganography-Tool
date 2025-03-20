# Steganography Tool

![Steganography](https://example.com/steganography-banner.jpg)

## Introduction

Steganography is the practice of concealing messages or information within other non-secret text or data. This tool allows you to hide and retrieve messages within image files using Python.

# Steganography Tool

## Overview
The Steganography Tool is a Python-based utility for embedding and extracting hidden data within JPEG images. This tool leverages the JPEG file structure to covertly store various types of data, such as text, images, and executable files, making it an effective means for secure data transmission.
![image](https://github.com/user-attachments/assets/fdb5cda5-323a-43c5-a21e-7104e1fe9168)

## Features
- **Text Steganography**: Embed and extract hidden text within JPEG images.
- **Image Steganography**: Embed and extract hidden PNG images within JPEG images.
- **Executable Steganography**: Embed and extract executable files within JPEG images.
- **System Compatibility**: Works seamlessly on major operating systems including Windows, macOS, and Linux.

## Getting Started

### Prerequisites
- Python 3.6 or higher
- Pillow Library
- BytesIO Module

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/elithaxxor/Steganography-Tool.git
    cd Steganography-Tool
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

#### Embedding Text in a JPEG Image
To embed text into a JPEG image, use the `add_text` function:
```python
from steganography_tool import AddText

image_path = 'example.jpg'
text_to_hide = 'This is a hidden message.'
AddText.add_text(image_path, text_to_hide)
cd Steganography-Tool
