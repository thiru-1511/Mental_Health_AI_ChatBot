import time
import base64
import numpy as np
from PIL import Image
import io
from mood_detector import MoodDetector

def create_test_image_base64():
    # Create a simple RGB image
    img = Image.new('RGB', (300, 300), color = (73, 109, 137))
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def benchmark():
    print("Starting MoodDetector Speed Benchmark...")
    detector = MoodDetector()
    
    test_img = create_test_image_base64()
    
    # Warm up (DeepFace might load models on first call)
    print("Performing warm-up call (this might take a moment)...")
    try:
        detector.detect_emotion(test_img)
    except Exception as e:
        print(f"Warm-up failed (expected if no face): {e}")

    # Actual measurement
    print("\nMeasuring detection speed...")
    start_time = time.time()
    # Note: facial detection will likely fail on a solid color image, 
    # but we want to measure how fast the 'opencv' backend processes it compared to 'retinaface'.
    detector.detect_emotion(test_img)
    end_time = time.time()
    
    print(f"\nFinal Detection Loop took: {end_time - start_time:.4f}s")
    print("Note: 'retinaface' usually takes 5-10s on CPU, while 'opencv' takes < 1s.")

if __name__ == "__main__":
    benchmark()
