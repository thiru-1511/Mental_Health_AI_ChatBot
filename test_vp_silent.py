import io
import wave
import traceback
from voice_processor import voice_processor

def create_dummy_wav():
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(b'\x00\x00' * 16000) # 1 second of silence
    blob = buffer.getvalue()
    return blob

wav_bytes = create_dummy_wav()

print("Starting analysis of dummy wav...")
try:
    result = voice_processor.analyze_audio(wav_bytes)
    print("Result:", result)
except Exception as e:
    print("Exception caught:")
    traceback.print_exc()
