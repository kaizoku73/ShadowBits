from PIL import Image
import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from crypto.aes import derive_key
import os

### To varify if the iamge is valid
def valid_img(cover_path):
    try:
        with Image.open(cover_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def embed_file(cover_path, payload_path, out_path, key=None, encrypt=False):

    out = random.randint(13478329543, 999999999999)
    temp = None

    try:
        if not os.path.exists(cover_path):
            raise FileNotFoundError(f"Cover image {cover_path} not found.")
        if not os.path.exists(payload_path):
            raise FileNotFoundError(f"Payload file {payload_path} not found.")
        if not valid_img(cover_path):
            raise ValueError(f"{cover_path} is not a valid image file.")
        
        temp_id = random.randint(12345678, 999999999)
        temp = f"temp_img_{temp_id}.png"

        try:
            with Image.open(cover_path) as img:
                img.save(temp, 'PNG')
            cover = temp
        except Exception as e:
            raise ValueError(f"Error converting cover image to PNG : {e}")
            

        img = Image.open(cover)
        mode = img.mode

        if mode != 'RGB':
            img = img.convert('RGB')

        pixels = list(img.getdata())

        with open(payload_path, 'rb') as f:
            payload = f.read()

        if encrypt:
            cipher = AES.new(derive_key(key), AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(payload)
            payload = cipher.nonce + tag + ciphertext

        starting = b'###START###'
        ending = b'###END###'

        length = len(payload).to_bytes(4, 'big')
        data = starting + length + payload + ending

        bits = ''.join(f'{byte:08b}' for byte in data)

        max_bits = len(pixels) * 3 ### 3 color channels per pixel
        if len(bits) > max_bits:
            raise ValueError('Payload too large to embed in cover image.')

        prng = random.Random(key)
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

        if os.path.exists(out_path):
            name, ext = os.path.splitext(out_path)
            counter = 1
            while os.path.exists(f"{name}_{counter}{ext}"):
                counter += 1
            out_path = f"{name}_{counter}{ext}"

        img.putdata(new_pixels)
        img.save(out_path)

        return out_path
    except Exception as e:
        print(f"Error in embedding : {e}")
        raise

    finally:
        if temp and os.path.exists(temp):
            try:
                os.remove(temp)
            except Exception as e:
                print(f"Could not remove the temporary file {temp} : {e}")