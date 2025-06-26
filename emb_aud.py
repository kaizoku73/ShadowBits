import wave
import ffmpeg
import random
from Crypto.Cipher import AES
from crypto.aes import derive_key
import os

def valid_wav(cover_path):
    try:
        with wave.open(cover_path, 'rb') as wave_file:
            params = wave_file.getparams() #try to read the basic params ,if it fails, its not valid wave file
            wave_file.readframes(min(1024, wave_file.getnframes()))
            return True
    except (wave.Error, EOFError):
        return False

def to_wav(input, output_file):
    try:
        output = f"{output_file}.wav"
        if os.path.exists(output):
            counter = 1
            while os.path.exists(f"{output_file}_{counter}.wav"):
                counter += 1
            output = f"{output_file}_{counter}.wav"
            
        ffmpeg.input(input).output(output, format='wav').run(overwrite_output=False, quiet=True)
        return output
    
    except ffmpeg.Error as e:
        print(f"Error converting file:{e}")
        raise

def embed_audio(cover_path, payload_path, out_path, key=None, encrypt=False):
    
    try:
        if not valid_wav(cover_path):
            raise ValueError(f"{cover_path} is not a valid WAV file")
        
        with wave.open(cover_path, mode='rb') as song:
            frame_bytes = bytearray(song.readframes(song.getnframes()))
            params = song.getparams()

        with open(payload_path, 'rb') as f:
            payload = f.read()

        if encrypt:
            cipher = AES.new(derive_key(key), AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(payload)
            payload = cipher.nonce + tag + ciphertext

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


        for i, bit in enumerate(payload_bits):
            frame_bytes[i] = (frame_bytes[i] & 0xFE) | bit

        output_path = f"{out_path}"
        if os.path.exists(output_path):
            counter = 1
            while os.path.exists(f"{out_path}_{counter}.wav"):
                counter += 1
            output_path = f"{out_path}_{counter}.wav"

        with wave.open(f'{output_path}', 'wb') as fd:
            fd.setparams(params)
            fd.writeframes(bytes(frame_bytes))

        return output_path
    
    except Exception as e:
        print(f"Error in embed_audio: {e}")
        raise
            
def combine(cover, secret, throw, key, encrypt=False):

    try:
        if not os.path.exists(cover):
            raise FileNotFoundError(f"Cover file path {cover} not found.")
        if not os.path.exists(secret):
            raise FileNotFoundError(f"Secret file path {secret} not found.")
        

        temp_id = random.randint(12487432,99999999)
        temp_file = f"converted_file_{temp_id}"
        
        #### Convert to wav format
        converted_wav = to_wav(cover, temp_file)

        try:

            result = embed_audio(converted_wav , secret, throw, key, encrypt=encrypt)
            return result
        
        finally:
            try:
                if os.path.exists(converted_wav):
                    os.remove(converted_wav) #### removes that converted file
            except Exception as e:
                print(f"Warning Could not remove temporary file {converted_wav}: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise