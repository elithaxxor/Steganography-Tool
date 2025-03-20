# Steganography Tool

[NOTE: Git is standalone or can be packaged] 

![Steganography](https://example.com/steganography-banner.jpg)

![image](https://github.com/user-attachments/assets/fdb5cda5-323a-43c5-a21e-7104e1fe9168)

```markdown
# JPEG Steganography Code Analysis

## Identified Functions

### `add_text`
- Appends text to an image file
- **Bug identified**: Code uses literal bytes string `b'input_text'` instead of converting the variable `input_text` to bytes

### `read_hidden`
- Extracts data appended after JPEG's EOI marker (FFD9)
- Finds FFD9 index, seeks to OFFSET+2, reads appended data

### `embed_image_hexData`
- Embeds a PNG image after JPEG's EOI marker
- Converts second image to PNG format
- Saves to BytesIO buffer
- Appends PNG data after original JPEG's FFD9 marker

### `read_embedded_image_hexData`
- Extracts embedded PNG image
- Locates FFD9 marker
- Seeks past it
- Uses PIL to read PNG data from bytes stream

### `embed_executable_file`
- Appends executable file contents after image
- Simply appends binary data to original image

### `retrieve_embedded_exec`
- Extracts embedded executable
- Finds FFD9
- Seeks past it
- Writes remaining data to new executable file 
```


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
```

### Embedding an Executable File in a JPEG Image

```
from steganography_tool import EmbedExecutableFile

image_path = 'example.jpg'
exec_path = 'hidden.exe'
EmbedExecutableFile.embed_executable_file(image_path, exec_path)
```
### Embedding an Image in a JPEG Image

To embed a PNG image into a JPEG image, use the embed_image_hexData function:
```python
from steganography_tool import EmbedImageHexData

jpeg_path = 'example.jpg'
png_path = 'hidden.png'
EmbedImageHexData.embed_image_hexData(jpeg_path, png_path)
```

### Extracting a Hidden Executable from a JPEG Image
```python
from steganography_tool import RetrieveEmbeddedExec

image_path = 'example.jpg'
output_exec_path = 'extracted.exe'
RetrieveEmbeddedExec.retrieve_embedded_exec(image_path, output_exec_path)

```

To extract a hidden executable file from a JPEG image, use the retrieve_embedded_exec function:

#### Extracting a Hidden Image from a JPEG Image
To extract a hidden PNG image from a JPEG image, use the read_embedded_image_hexData function:


```Python
from steganography_tool import ReadEmbeddedImageHexData

image_path = 'example.jpg'
hidden_image = ReadEmbeddedImageHexData.read_embedded_image_hexData(image_path)
hidden_image.show()
```
