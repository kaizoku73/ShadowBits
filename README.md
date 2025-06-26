# ShadowBits 🔒

A powerful steganography tool that allows you to hide files within images and audio files using LSB (Least Significant Bit) techniques. ShadowBits supports both embedding and extraction operations with optional AES encryption for enhanced security.

## Features

- **Image Steganography**: Hide files within PNG images using LSB manipulation
- **Audio Steganography**: Embed files in WAV audio files 
- **AES Encryption**: Optional encryption layer for embedded data
- **Key-based Randomization**: Uses secret keys to randomize bit placement for enhanced security
- **Multiple Format Support**: Automatically converts audio files to WAV format when needed
- **Collision Prevention**: Automatically handles filename conflicts during output

## Installation

### Prerequisites

```bash
pip install pillow pycryptodome ffmpeg-python
```

## Usage

ShadowBits provides a command-line interface with four main operations:

### Image Operations

#### Embed a file in an image
```bash
python cli.py img-embed --in secret.txt --cover image.png --out stego_image.png --key mysecretkey
```

#### Embed with encryption
```bash
python cli.py img-embed --in secret.txt --cover image.png --out stego_image.png --key mysecretkey --encrypt
```

#### Extract from image
```bash
python cli.py img-extract --stego stego_image.png --out extracted.txt --key mysecretkey
```

#### Extract with decryption
```bash
python cli.py img-extract --stego stego_image.png --out extracted.txt --key mysecretkey --decrypt
```

### Audio Operations

#### Embed a file in audio
```bash
python cli.py aud-embed --in secret.pdf --cover music.mp3 --out stego_audio.wav --key myaudiokey
```

#### Embed with encryption
```bash
python cli.py aud-embed --in secret.pdf --cover music.mp3 --out stego_audio.wav --key myaudiokey --encrypt
```

#### Extract from audio
```bash
python cli.py aud-extract --stego stego_audio.wav --out extracted.pdf --key myaudiokey
```

#### Extract with decryption
```bash
python cli.py aud-extract --stego stego_audio.wav --out extracted.pdf --key myaudiokey --decrypt
```

## How It Works

### LSB Steganography
ShadowBits uses the Least Significant Bit (LSB) method to hide data:

- **Images**: Modifies the least significant bit of RGB color channels
- **Audio**: Alters the least significant bit of audio sample data

## What is LSB and how does it work?
Article coming soon

### Security Features

1. **Key-based Randomization**: Uses PRNG seeded with your secret key to randomize bit placement
2. **AES Encryption**: Optional AES-EAX encryption with key derivation
3. **Data Integrity**: Uses start/end markers to ensure data completeness
4. **Format Validation**: Verifies file formats before processing

## Limitations

- **Image capacity**: Limited by image size (3 bits per pixel for RGB images)
- **Audio capacity**: Limited by audio file length (1 bit per sample)
- **Audio format**: Output audio files are always in WAV format
- **File size**: To hide larger files, you need larger cover media file

## Examples

### Hide a document in a photo
```bash
python cli.py img-embed --in document.pdf --cover vacation.jpg --out innocent_photo.png --key family2023 --encrypt
```

### Extract the hidden document
```bash
python cli.py img-extract --stego innocent_photo.png --out recovered_document.pdf --key family2023 --decrypt
```

### Hide source code in music
```bash
python cli.py aud-embed --in source_code.zip --cover favorite_song.mp3 --out normal_audio.wav --key coding123
```

## Security Considerations

- **Key Management**: Use strong, unique keys for each operation
- **Cover Selection**: Choose cover files with sufficient capacity
- **Encryption**: Always use `--encrypt` for sensitive data
- **Key Reuse**: Avoid reusing keys across different files

## Error Handling

ShadowBits includes comprehensive error handling for:
- Invalid file formats
- Insufficient cover media capacity  
- Corrupted embedded data
- Decryption failures
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
