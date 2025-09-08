def detect_file_type(data):
    """
    Detect file type based on magic bytes (file signatures)
    Returns tuple: (extension, mime_type)
    """
    if not data or len(data) < 4:
        return 'bin', 'application/octet-stream'
    
    # Common file signatures
    signatures = {
        # Images
        b'\xFF\xD8\xFF': ('jpg', 'image/jpeg'),
        b'\x89PNG\r\n\x1a\n': ('png', 'image/png'),
        b'GIF87a': ('gif', 'image/gif'),
        b'GIF89a': ('gif', 'image/gif'),
        b'BM': ('bmp', 'image/bmp'),
        b'RIFF': ('webp', 'image/webp'),
        b'\x00\x00\x01\x00': ('ico', 'image/x-icon'),
        
        # Documents
        b'%PDF': ('pdf', 'application/pdf'),
        b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1': ('doc', 'application/msword'),
        b'PK\x03\x04': ('zip', 'application/zip'),  # Also docx, xlsx, etc.
        
        # Audio
        b'ID3': ('mp3', 'audio/mpeg'),
        b'\xFF\xFB': ('mp3', 'audio/mpeg'),
        b'\xFF\xF3': ('mp3', 'audio/mpeg'),
        b'\xFF\xF2': ('mp3', 'audio/mpeg'),
        b'OggS': ('ogg', 'audio/ogg'),
        b'fLaC': ('flac', 'audio/flac'),
        
        # Video
        b'\x00\x00\x00\x18ftypmp4': ('mp4', 'video/mp4'),
        b'\x00\x00\x00\x20ftypM4V': ('m4v', 'video/x-m4v'),
        b'RIFF....AVI ': ('avi', 'video/x-msvideo'),
        
        # Archives
        b'\x50\x4B\x05\x06': ('zip', 'application/zip'),
        b'\x50\x4B\x07\x08': ('zip', 'application/zip'),
        b'\x1F\x8B\x08': ('gz', 'application/gzip'),
        b'Rar!\x1A\x07\x00': ('rar', 'application/x-rar-compressed'),
        b'7z\xBC\xAF\x27\x1C': ('7z', 'application/x-7z-compressed'),
        
        # Text/Code
        b'#!/bin/bash': ('sh', 'text/x-shellscript'),
        b'#!/bin/sh': ('sh', 'text/x-shellscript'),
        b'<?xml': ('xml', 'text/xml'),
        b'<html': ('html', 'text/html'),
        b'<!DOCTYPE html': ('html', 'text/html'),
    }
    
    for sig, (ext, mime) in signatures.items():
        if data.startswith(sig):
            # Special handling for RIFF files
            if sig == b'RIFF' and len(data) >= 12:
                if data[8:12] == b'WAVE':
                    return 'wav', 'audio/wav'
                elif data[8:12] == b'WEBP':
                    return 'webp', 'image/webp'
                elif data[8:12] == b'AVI ':
                    return 'avi', 'video/x-msvideo'
            return ext, mime
    
    # Check for text files
    try:
        text = data[:min(512, len(data))].decode('utf-8', errors='strict')
        if all(ord(c) < 127 and (c.isprintable() or c.isspace()) for c in text):
            # Further classify text files
            text_lower = text.lower()
            if any(keyword in text_lower for keyword in ['<html', '<!doctype', '<head', '<body']):
                return 'html', 'text/html'
            elif text.strip().startswith('<?xml'):
                return 'xml', 'text/xml'
            elif any(keyword in text_lower for keyword in ['import ', 'def ', 'class ', 'if __name__']):
                return 'py', 'text/x-python'
            elif any(keyword in text_lower for keyword in ['#include', 'int main', 'void ']):
                return 'c', 'text/x-c'
            elif any(keyword in text_lower for keyword in ['function', 'var ', 'let ', 'const ']):
                return 'js', 'text/javascript'
            else:
                return 'txt', 'text/plain'
    except UnicodeDecodeError:
        pass
    
    # If no signature matches, return binary
    return 'bin', 'application/octet-stream'