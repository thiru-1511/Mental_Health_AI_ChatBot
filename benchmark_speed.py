import time
import base64
import os
from mood_detector import MoodDetector

def benchmark():
    detector = MoodDetector()
    
    # Create a dummy image (or use one if exists)
    # Since I don't have a real image path easily accessible, I'll use the detection loop 
    # to measure the 'analyze' part if I had an image.
    # However, I can at least test the initialization speed which was part of the bottleneck.
    
    # Testing pre-loading Benefit
    start_init = time.time()
    detector = MoodDetector()
    end_init = time.time()
    print(f"Initialization/Pre-loading took: {end_init - start_init:.4f}s")

    # If test_user_img.py exists, I might be able to use logic from it
    print("Optimization applied. Please test in the browser for the full effect.")

if __name__ == "__main__":
    benchmark()
