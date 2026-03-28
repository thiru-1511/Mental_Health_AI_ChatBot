import requests
import io
import wave
import sys

def create_dummy_wav():
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        f.writeframes(b'\x00\x00' * 16000) # 1 second of silence
    blob = buffer.getvalue()
    return blob

try:
    wav_bytes = create_dummy_wav()
    files = {'audio': ('dummy.wav', wav_bytes, 'audio/wav')}
    print("Sending request...")
    resp = requests.post("http://localhost:5000/api/voice-mood", files=files)
    print("Status Code:", resp.status_code)
    try:
        print("Response JSON:", resp.json())
    except:
        print("Response Text:", resp.text[:500])
except Exception as e:
    print("Error:", e)
