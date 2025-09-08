from PIL import Image
import random
from crypto.aes import *
import os
from emb_img import valid_img
from validator import detect_file_type
import time

def extract_file(stego_path, key):
    start = time.time()
    try:
        if not os.path.exists(stego_path):
            raise FileNotFoundError(f"stego image {stego_path} not found.")
        if not valid_img(stego_path):
            raise ValueError(f"Image is not a valid PNG file.")
        
        print("Loading stego file...")
        img = Image.open(stego_path)
        pixels = list(img.getdata())
        
        seed = to_seed(key)
        prng = random.Random(seed)
        indexes = list(range(len(pixels)))
        prng.shuffle(indexes)

        print("Extracting the bits from stego file...")
        bits = ''
        for i in range(len(pixels)):
            pixel_idx = indexes[i]  
            r, g, b = pixels[pixel_idx]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    
        if len(bits) % 8 != 0:
            bits = bits[:-(len(bits) % 8)]  # Remove incomplete byte
        
        print("Converting bits into bytes...")
        bytes_list = bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])
        
        starting = b'###START###'
        ending = b'###END###'

        print("Locating markers in bytes...")
        start_point = bytes_list.find(starting)
        if start_point == -1:
            raise ValueError("Starting marker of the payload not found in image or key is incorrect")
        
        data_start = start_point + len(starting)

        if len(bytes_list) < data_start + 4:
            raise ValueError("Not enough data to extract length")
        
        length = int.from_bytes(bytes_list[data_start:data_start + 4], 'big')

        payload_start = data_start + 4
        payload_end = payload_start + length    
    
        if len(bytes_list) < payload_end:
            raise ValueError(f"Not enough data to extract payload of length {length}")
        
        print("Extracting payload's bytes from bytes...")
        payload = bytes_list[payload_start:payload_end]

        print("Verifying the end marker in bytes...") 
        end_start = payload_end
        end_end = end_start + len(ending)

        if len(bytes_list) < end_end:
            raise ValueError(f"Not enough data to verify the end marker.")
        
        extract_end = bytes_list[end_start:end_end]
        if extract_end != ending:
            raise ValueError(f"End marker not found or corrupted")
        
        print("Decrypting the payload bytes...")
        payload = decryption(payload, key)
            
        extension, mime_type = detect_file_type(payload)
        out_path = f"extracted_file.{extension}"

        print("Saving the extracted file...")
        with open(out_path, 'wb') as f:
            f.write(payload)
        end = time.time() - start
        print(f"Time taken: {int(end)} seconds.")
        return out_path
    except Exception as e:
        print(f"Error in extracion : {e}")
        raise