import numpy as np
from deepface import DeepFace
import cv2
import os

def test_detection():
    # Create a dummy blank image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(img, "Test", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    print("Testing DeepFace.analyze...")
    try:
        result = DeepFace.analyze(
            img_path=img,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv',
            silent=True
        )
        print("Detection successful!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Detection failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_detection()
