import wave
import random
from crypto.aes import *
import os
import time

def valid_wav(cover_path):
    try:
        with wave.open(cover_path, 'rb') as wave_file:
            channels = wave_file.getnchannels()
            sample_width = wave_file.getsampwidth()
            framerate = wave_file.getframerate()
            frames = wave_file.getnframes()
            
            if not (1 <= channels <= 8): 
                return False
            if sample_width not in [1, 2, 3, 4]:
                return False
            if not (8000 <= framerate <= 192000):
                return False
            if frames <= 0:
                return False
            
            wave_file.readframes(min(1024, frames))
            
            return True
            
    except (wave.Error, EOFError, FileNotFoundError, PermissionError):
        return False
    except Exception:
        return False


def embed_audio(cover_path, payload_path, key):
    start = time.time()
    try:
        if not os.path.exists(cover_path):
            raise FileNotFoundError(f"Cover file path {cover_path} not found.")
        if not os.path.exists(payload_path):
            raise FileNotFoundError(f"Secret file path {payload_path} not found.")
        if not valid_wav(cover_path):
            raise ValueError(f"{cover_path} is not a valid WAV file")
        
        print("Loading cover file...")
        with wave.open(cover_path, mode='rb') as song:
            frame_bytes = bytearray(song.readframes(song.getnframes()))
            params = song.getparams()

        print("Loading payload file...")
        with open(payload_path, 'rb') as f:
            payload = f.read()

        print("Encrypting the payload's byte...")
        payload = encryption(payload, key)

        print("Attaching the markers on payload's bytes...")
        starting = b'###START###'
        ending = b'###END###'
        full_payload = starting + payload + ending

        print("Converting the payload's byte into bits...")
        payload_bits = []
        for byte in full_payload:
            bits = format(byte, '08b')
            payload_bits.extend([int(b) for b in bits])

        print("Checking cover file capacity...")
        max_payload_bits = len(frame_bytes)
        if len(payload_bits) > max_payload_bits:
            raise ValueError(f"Payload too large! Need {len(payload_bits)} bits but only have {max_payload_bits} available")

        seed = to_seed(key)
        shifu = random.Random(seed)
        indexes = list(range(len(frame_bytes)))
        shifu.shuffle(indexes)

        print("Embedding the payload bits into cover file bytes...")
        for bit_idx, bit in enumerate(payload_bits):
            i = indexes[bit_idx]
            frame_bytes[i] = (frame_bytes[i] & 0xFE) | bit

        output_path = "encoded.wav"
        if os.path.exists(output_path):
            counter = 1
            while os.path.exists(f"encoded({counter}).wav"):
                counter += 1
            output_path = f"encoded({counter}).wav"

        print("Saving stego file...")
        with wave.open(output_path, 'wb') as fd:
            fd.setparams(params)
            fd.writeframes(bytes(frame_bytes))
        end = time.time() - start
        print(f"Time taken: {int(end)} seconds.")
        return output_path
    
    except Exception as e:
        print(f"Error in embed_audio: {e}")
        raise