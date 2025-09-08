import wave
from emb_aud import valid_wav
from crypto.aes import *
import os
import random
from validator import detect_file_type
import time

def extract_audio(stego_path, key):
    start = time.time()
    try:
        if not valid_wav(stego_path):
            raise ValueError(f"{stego_path} is not a valid wav file")
        
        print("Loading stego file...")
        with wave.open(stego_path, 'rb') as song:
            frame_bytes = song.readframes(song.getnframes())

        seed = to_seed(key)
        shifu = random.Random(seed)
        indexes = list(range(len(frame_bytes)))
        shifu.shuffle(indexes)

        print("Extracting the bits from stego file...")
        extracted_bits = []
        for i in indexes:
            extracted_bits.append(frame_bytes[i] & 1)

        print("Converting extracted bits into bytes...")
        extracted_bytes = bytearray()
        for i in range(0, len(extracted_bits), 8):
            if i + 7 < len(extracted_bits):
                byte_bits = extracted_bits[i:i+8]
                byte_value = 0
                for j, bit in enumerate(byte_bits):
                    byte_value |= bit << (7-j)
                extracted_bytes.append(byte_value)

        starting = b'###START###'
        ending = b'###END###'
        print("Locating markers in bytes...")
        try:
            start_byte = extracted_bytes.find(starting)
            if start_byte == -1:
                raise ValueError("Starting point not found - file may not contain embedded data or key is incorrect")
            
            search = start_byte + len(starting)
            end_byte = extracted_bytes.find(ending, search)
            if end_byte == -1:
                raise ValueError("Ending point not found - embedded data maybe corrupted")
            
            print("Extracting payload's bytes from bytes....")
            payload = bytes(extracted_bytes[search:end_byte])

        except Exception as e:
            print(f"Error finding payload data : {e}")
            return None
        
        print("Decrypting the payload's bytes...")
        payload = decryption(payload, key)
            
        extension, mime_type = detect_file_type(payload)
        output_path = f"hidden_file.{extension}"

        print("Saving the extracted file...")
        with open(output_path, 'wb') as fd:
            fd.write(payload)
        end = time.time() - start
        print(f"Time taken: {int(end)} seconds.")
        return payload
    
    except Exception as e:
        print(f"Error in extracting data from file: {e}")
        return None