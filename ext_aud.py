import wave
from emb_aud import valid_wav
from Crypto.Cipher import AES
from crypto.aes import derive_key
import os

def extract_audio(stego_path, output_path, key, decrypt=False):

    try:
        if not valid_wav(stego_path):
            raise ValueError(f"{stego_path} is not a valid wav file")
        
        with wave.open(stego_path, 'rb') as song:
            frame_bytes = song.readframes(song.getnframes())

        ### Extracts Last bits of every byte
        extracted_bits = []
        for byte in frame_bytes:
            extracted_bits.append(byte & 1)

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
                raise ValueError("Starting point not found - file may not contain embedded data")
            
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
            try:
                nonce = payload[:16]
                tag = payload[16:32]
                ciphertext = payload[32:]
                cipher = AES.new(derive_key(key), AES.MODE_EAX, nonce=nonce)
                payload = cipher.decrypt_and_verify(ciphertext, tag)

            except Exception as e:
                print(f"Decryption failed : {e}")
                return None
            

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

        print(f"Successfully extracted {len(payload)} bytes to {output_path}")
        return payload
    
    except Exception as e:
        print(f"Error in extracting data from file: {e}")
        return None