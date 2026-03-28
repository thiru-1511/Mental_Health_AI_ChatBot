import io
import wave
import traceback
import struct

from app import voice_processor, mood_detector, wellness_manager, mood_tracker

def create_valid_wav():
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(16000)
        import math
        frames = bytearray()
        for i in range(16000):
            val = int(math.sin(2.0 * math.pi * 440.0 * i / 16000) * 30000)
            frames.extend(struct.pack('<h', val))
        f.writeframes(frames)
    return buffer.getvalue()

wav_bytes = create_valid_wav()

try:
    print("1. Analyzing audio...")
    result = voice_processor.analyze_audio(wav_bytes)
    print("Result:", result)
    if result.get('success'):
        emotion = result['emotion']
        print(f"2. Getting songs for {emotion}...")
        songs = mood_detector.get_song_recommendations(emotion)
        print(f"Songs:", len(songs))
        
        print("3. Getting wellness plan...")
        wellness = wellness_manager.get_wellness_plan(emotion)
        print("Wellness keys:", wellness.keys())
        
        print("4. Logging mood...")
        mood_tracker.log_mood(emotion, confidence=result.get('confidence'), source="voice")
        print("Mood logged successfully.")
except Exception as e:
    print("Exception caught:")
    traceback.print_exc()
