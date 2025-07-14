import wave
from emb_aud import valid_wav
from crypto.aes import *
import os
import random

def extract_audio(stego_path, output_path, key, decrypt=False):

    try:
        if not valid_wav(stego_path):
            raise ValueError(f"{stego_path} is not a valid wav file")
        
        with wave.open(stego_path, 'rb') as song:
            frame_bytes = song.readframes(song.getnframes())

        ### Extracts Last bits of randomized byte
        seed = to_seed(key)
        shifu = random.Random(seed)
        indexes = list(range(len(frame_bytes)))
        shifu.shuffle(indexes)

        extracted_bits = []
        for i in indexes:
            extracted_bits.append(frame_bytes[i] & 1)

        ### convert bits back to bytes
        extracted_bytes = bytearray()
        for i in range(0, len(extracted_bits), 8):
            if i + 7 < len(extracted_bits):
                byte_bits = extracted_bits[i:i+8]
                byte_value = 0
                for j, bit in enumerate(byte_bits):
                    byte_value |= bit << (7-j)
                extracted_bytes.append(byte_value)

        ### find starting and ending of the embedded payload
        starting = b'###START###'
        ending = b'###END###'

        try:
            start_byte = extracted_bytes.find(starting)
            if start_byte == -1:
                raise ValueError("Starting point not found - file may not contain embedded data or key is incorrect")
            
            search = start_byte + len(starting)
            end_byte = extracted_bytes.find(ending, search)
            if end_byte == -1:
                raise ValueError("Ending point not found - embedded data maybe corrupted")
            
            payload = bytes(extracted_bytes[search:end_byte])

        except Exception as e:
            print(f"Error finding hidden data : {e}")
            return None
        
        ### Decrypt if provided encryption duting embedding
        if decrypt:
            payload = decryption(payload, key)
            
        ### create out file
        if os.path.exists(output_path):
            name, ext = os.path.splitext(output_path)
            counter = 1
            while os.path.exists(f"{name}_{counter}{ext}"):
                counter += 1

            output_path = f"{name}_{counter}{ext}"

        ### save the payload
        with open(output_path, 'wb') as fd:
            fd.write(payload)

        return payload
    
    except Exception as e:
        print(f"Error in extracting data from file: {e}")
        return None