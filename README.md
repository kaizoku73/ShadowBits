# ShadowBits 🔒

A powerful steganography tool that allows you to hide files within images and audio files using LSB (Least Significant Bit) techniques. ShadowBits supports both embedding and extraction operations with optional AES encryption for enhanced security.

## Features

- **Image Steganography**: Hide files within PNG images using LSB manipulation
- **Audio Steganography**: Embed files in WAV audio files 
- **AES Encryption**: Optional encryption layer for embedded data
- **Key-based Randomization**: Uses secret keys to randomize bit placement for enhanced security
- **Automatic File Type Detection**: Detects and preserves original file types during extraction
- **Format Validation**: Validates PNG images and WAV audio files before processing
- **Collision Prevention**: Automatically handles filename conflicts during output
- **Comprehensive Error Handling**: Robust error handling for various failure scenarios

## Installation

### Prerequisites

```bash
pip install -r requirements.txt
```

## Usage

ShadowBits provides a command-line interface with four main operations:

### Image Operations

#### Embed a file in an image
```bash
python cli.py img-embed --in secret.txt --cover image.png --key mysecretkey
```

#### Extract from image
```bash
python cli.py img-extract --stego stego_image.png --key mysecretkey
```


### Audio Operations

#### Embed a file in audio
```bash
python cli.py aud-embed --in secret.pdf --cover music.wav --key myaudiokey
```

#### Extract from audio
```bash
python cli.py aud-extract --stego stego_audio.wav --key myaudiokey
```

## How It Works

### LSB Steganography
ShadowBits uses the Least Significant Bit (LSB) method to hide data:

- **Images**: Modifies the least significant bit of RGB color channels in a randomized order
- **Audio**: Modifies the least significant bit of audio sample data in a randomized pattern

## What is LSB and how does it work?
For a detailed explanation of LSB steganography and how it works, check out this article: https://kaizoku.gitbook.io/steganography

### Security Features

1. **Key-based Randomization**: Uses PRNG seeded with your secret key to randomize bit placement
2. **Automatic AES Encryption**: All data is encrypted using AES-EAX mode with SHA-256 key derivation
3. **Data Integrity Markers**: Uses start/end markers to ensure data completeness
4. **Format Validation**: Verifies PNG/WAV file formats before processing
5. **File Type Detection**: Automatically detects original file type using magic bytes for proper restoration

## Hidden Files
The tool can hide any file type and will automatically detect and restore the original format using magic byte signatures, including:
- Images: JPG, PNG, GIF, BMP, WebP, ICO
- Documents: PDF, DOC, ZIP archives
- Audio: MP3, OGG, FLAC, WAV
- Video: MP4, M4V, AVI
- Archives: ZIP, GZ, RAR, 7Z
- Text/Code: HTML, XML, Python, C, JavaScript, plain text
- Binary files: Any other format as .bin


## Limitations

- **Image capacity**: Limited by image size (3 bits per pixel for RGB images)
- **Audio capacity**: Limited by audio file length (1 bit per sample)
- **File size**: To hide larger files, you need larger cover media file

## Examples

### Hide a document in a photo
```bash
python cli.py img-embed --in document.pdf --cover vacation.jpg --key family2023
```

### Extract the hidden document
```bash
python cli.py img-extract --stego stego_file.png --key family2023
```

### Hide source code in music
```bash
python cli.py aud-embed --in source_code.zip --cover favorite_song.mp3 --key coding123
```

## Security Considerations

- **Key Management**: Use strong, unique keys for each operation
- **Key Security**: The same key is used for both encryption and randomization
- **Cover Selection**: Choose cover files with sufficient capacity for your payload
- **File Format**: Ensure cover images are PNG and audio files are WAV
- **Key Reuse**: Avoid reusing keys across different files

## Error Handling

ShadowBits includes comprehensive error handling for:
- Invalid file formats
- Insufficient cover media capacity  
- Corrupted embedded data or invalid markers
- AES Decryption failures (wrong key or corrupted data)
- Missing files or permissions

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is open source, feel free to use and modify it. Just don't forget to credit me if you share it!

## Disclaimer

This tool is for educational and legitimate purposes only. Users are responsible for ensuring compliance with applicable laws and regulations when using steganography techniques.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**ShadowBits** - Where your secrets hide in plain sight 👁️‍🗨️

**Made by kaizoku**
