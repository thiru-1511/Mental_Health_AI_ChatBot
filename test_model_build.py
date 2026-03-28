from deepface import DeepFace
try:
    print("Trying build_model('Emotion')...")
    DeepFace.build_model('Emotion')
    print("Success with 'Emotion'")
except Exception as e:
    print(f"Failed with 'Emotion': {e}")

try:
    print("Trying build_model('emotion')...")
    DeepFace.build_model('emotion')
    print("Success with 'emotion'")
except Exception as e:
    print(f"Failed with 'emotion': {e}")
