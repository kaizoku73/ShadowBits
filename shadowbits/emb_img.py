from PIL import Image
import random
from .crypto.aes import *
import os
import time

### To varify if the image is valid
def valid_img(cover_path):
    try:
        with Image.open(cover_path) as img:
            # Check format first
            if img.format and img.format.upper() == "PNG":
                img.verify()  # Only verify if it claims to be PNG
                return True
            return False
    except Exception:
        return False


def embed_file(cover_path, payload_path, key):
    start = time.time()
    try:
        if not os.path.exists(cover_path):
            raise FileNotFoundError(f"Cover image {cover_path} not found.")
        if not os.path.exists(payload_path):
            raise FileNotFoundError(f"Payload file {payload_path} not found.")
        if not valid_img(cover_path):
            raise ValueError(f"{cover_path} is not a valid PNG image file.")

        print("Loading cover file...")
        img = Image.open(cover_path)
        mode = img.mode

        if mode != 'RGB':
            print(f"Converting the {mode} mode to RGB mode...")
            img = img.convert('RGB')

        pixels = list(img.getdata())

        print("Loading payload file in bytes...")
        with open(payload_path, 'rb') as f:
            payload = f.read()

        print("Encrypting the payload bytes...")
        payload = encryption(payload, key)

        print("Attaching the markers on payload bytes...")
        starting = b'###START###'
        ending = b'###END###'

        length = len(payload).to_bytes(4, 'big')
        data = starting + length + payload + ending

        print("Convertng payload bytes into bits...")
        bits = ''.join(f'{byte:08b}' for byte in data)

        max_bits = len(pixels) * 3 ### 3 color channels per pixel
        print("Checking cover file capacity...")
        if len(bits) > max_bits:
            raise ValueError('Payload is too large to embed in cover file.')

        seed = to_seed(key)
        prng = random.Random(seed)
        indexes = list(range(len(pixels)))
        prng.shuffle(indexes)

        print("Embedding data into image...")
        new_pixels = [None] * len(pixels)  
        bit_idx = 0
        
        for i in range(len(indexes)):
            pixel_idx = indexes[i]  
            r, g, b = pixels[pixel_idx]
        
            if bit_idx < len(bits):
                r = (r & ~1) | int(bits[bit_idx])
                bit_idx += 1
            if bit_idx < len(bits):
                g = (g & ~1) | int(bits[bit_idx])
                bit_idx += 1
            if bit_idx < len(bits):
                b = (b & ~1) | int(bits[bit_idx])
                bit_idx += 1

            new_pixels[pixel_idx] = (r, g, b)

        img.putdata(new_pixels)

        output_path = "stego_file.png"
        if os.path.exists(output_path):
            counter = 1
            while os.path.exists(f"stego_file({counter}).png"):
                counter += 1
            output_path = f"stego_file({counter}).png"
            
        print("Saving the stego file...")
        file = img.save(output_path)
        end = time.time() - start
        print(f"Time taken: {int(end)} seconds.")
        return file
    except Exception as e:
        print(f"Error in embedding : {e}")
        raise