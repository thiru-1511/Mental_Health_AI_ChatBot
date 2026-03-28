import numpy as np
from deepface import DeepFace
import cv2
import os

def test_detection():
    img_path = r"C:/Users/thirumalai/.gemini/antigravity/brain/5397d8b6-d5c2-474d-b284-04ea9ec211e4/uploaded_media_1771515871897.png"
    
    print(f"Testing DeepFace.analyze on {img_path}...")
    try:
        if not os.path.exists(img_path):
            print("Image file not found!")
            return

        result = DeepFace.analyze(
            img_path=img_path,
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
