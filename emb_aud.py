import wave
import random
from crypto.aes import *
import os

def valid_wav(cover_path):
    try:
        with wave.open(cover_path, 'rb') as wave_file:
            wave_file.readframes(min(1024, wave_file.getnframes()))
            return True
    except (wave.Error, EOFError):
        return False


def embed_audio(cover_path, payload_path, out_path, key, encrypt=False):
    
    try:
        if not os.path.exists(cover_path):
            raise FileNotFoundError(f"Cover file path {cover_path} not found.")
        if not os.path.exists(payload_path):
            raise FileNotFoundError(f"Secret file path {payload_path} not found.")
        if not valid_wav(cover_path):
            raise ValueError(f"{cover_path} is not a valid WAV file")
        
        with wave.open(cover_path, mode='rb') as song:
            frame_bytes = bytearray(song.readframes(song.getnframes()))
            params = song.getparams()

        with open(payload_path, 'rb') as f:
            payload = f.read()

        if encrypt:
            payload = encryption(payload, key)

        starting = b'###START###'
        ending = b'###END###'
        full_payload = starting + payload + ending

        payload_bits = []
        for byte in full_payload:
            bits = format(byte, '08b')
            payload_bits.extend([int(b) for b in bits])

        #check if audio file has enough space to hold the payload
        max_payload_bits = len(frame_bytes)
        if len(payload_bits) > max_payload_bits:
            raise ValueError(f"Payload too large! Need {len(payload_bits)} bits but only have {max_payload_bits} available")

        seed = to_seed(key)
        shifu = random.Random(seed)
        indexes = list(range(len(frame_bytes)))
        shifu.shuffle(indexes)

        for bit_idx, bit in enumerate(payload_bits):
            i = indexes[bit_idx]
            frame_bytes[i] = (frame_bytes[i] & 0xFE) | bit

        if not out_path.lower().endswith('.wav'):
            out_path += '.wav'

        output_path = out_path
        if os.path.exists(output_path):
            name, ext = os.path.splitext(out_path)
            counter = 1
            while os.path.exists(f"{name}_{counter}{ext}"):
                counter += 1
            output_path = f"{name}_{counter}{ext}"

        with wave.open(output_path, 'wb') as fd:
            fd.setparams(params)
            fd.writeframes(bytes(frame_bytes))

        return output_path
    
    except Exception as e:
        print(f"Error in embed_audio: {e}")
        raise