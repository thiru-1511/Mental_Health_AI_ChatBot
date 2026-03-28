import urllib.request
import urllib.parse
import io
import wave

def create_dummy_wav():
    import struct
    import math
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        frames = bytearray()
        for i in range(16000):
            val = int(math.sin(2.0 * math.pi * 440.0 * i / 16000) * 30000)
            frames.extend(struct.pack('<h', val))
        f.writeframes(frames)
    return buffer.getvalue()

wav_bytes = create_dummy_wav()

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = (
    b'--' + boundary.encode() + b'\r\n'
    b'Content-Disposition: form-data; name="audio"; filename="recording.wav"\r\n'
    b'Content-Type: audio/wav\r\n\r\n' +
    wav_bytes +
    b'\r\n--' + boundary.encode() + b'--\r\n'
)

req = urllib.request.Request(
    'http://localhost:5000/api/voice-mood',
    data=body,
    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
)

try:
    print("Sending request...")
    with urllib.request.urlopen(req) as response:
        print("Status", response.status)
        print("Response", response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Body:", e.read().decode())
except Exception as e:
    print("Error:", e)
