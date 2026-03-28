import io
import wave
import traceback
import struct
from voice_processor import voice_processor

def create_valid_wav():
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        # 1 sec of 440Hz sine wave to make sure it's valid
        import math
        frames = bytearray()
        for i in range(16000):
            val = int(math.sin(2.0 * math.pi * 440.0 * i / 16000) * 30000)
            frames.extend(struct.pack('<h', val))
        f.writeframes(frames)
    return buffer.getvalue()

wav_bytes = create_valid_wav()

print("Starting analysis...")
try:
    result = voice_processor.analyze_audio(wav_bytes)
    print("Result:", result)
except Exception as e:
    print("Exception caught:")
    traceback.print_exc()
