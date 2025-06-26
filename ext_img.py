from PIL import Image
import random
from Crypto.Cipher import AES
from crypto.aes import derive_key
import os

def extract_file(stego_path, out_path, key=None, decrypt=False):

    try:
        if not os.path.exists(stego_path):
            raise FileNotFoundError(f"stego image {stego_path} not found.")
        
        img = Image.open(stego_path)
        pixels = list(img.getdata())
        

        prng = random.Random(key)
        indexes = list(range(len(pixels)))
        prng.shuffle(indexes)

        bits = ''
        for i in range(len(pixels)):
            pixel_idx = indexes[i]  
            r, g, b = pixels[pixel_idx]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    
        if len(bits) % 8 != 0:
            bits = bits[:-(len(bits) % 8)]  # Remove incomplete byte
        
        bytes_list = bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])
        
        starting = b'###START###'
        ending = b'###END###'

        start_point = bytes_list.find(starting)
        if start_point == -1:
            raise ValueError("Starting point of the payload not found in image")
        
        data_start = start_point + len(starting)

        if len(bytes_list) < data_start + 4:
            raise ValueError("Not enough data to extract length")
        
        length = int.from_bytes(bytes_list[data_start:data_start + 4], 'big')

        payload_start = data_start + 4
        payload_end = payload_start + length    
    
        if len(bytes_list) < payload_end:
            raise ValueError(f"Not enough data to extract payload of length {length}")
        
        payload = bytes_list[payload_start:payload_end]

        ### verify the ending 
        end_start = payload_end
        end_end = end_start + len(ending)

        if len(bytes_list) < end_end:
            raise ValueError(f"Not enough data to verify the ending.")
        
        extract_end = bytes_list[end_start:end_end]
        if extract_end != ending:
            raise ValueError(f"Ending not found or corrupted")
        
        ### decryption
        if decrypt:
            if len(payload) < 32:
                raise ValueError("Encrypted payload too short")
            nonce = payload[:16]
            tag = payload[16:32]
            ciphertext = payload[32:]
            cipher = AES.new(derive_key(key), AES.MODE_EAX, nonce=nonce)
            try:
                payload = cipher.decrypt_and_verify(ciphertext, tag)
            except ValueError as e:
                raise ValueError("Decryption failed - wrong key or corrupted data")
            
        if os.path.exists(out_path):
            name, ext = os.path.splitext(out_path)
            counter = 1
            while os.path.exists(f"{name}_{counter}{ext}"):
                counter += 1
            out_path = f"{name}_{counter}{ext}"

        with open(out_path, 'wb') as f:
            f.write(payload)

        return out_path
    except Exception as e:
        print(f"Error in extracion : {e}")
        raise