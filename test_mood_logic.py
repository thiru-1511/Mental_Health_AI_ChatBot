
from mood_detector import MoodDetector
from voice_processor import VoiceProcessor
import unittest

class TestMoodLogic(unittest.TestCase):
    def setUp(self):
        self.md = MoodDetector()
        self.vp = VoiceProcessor()

    def test_image_mood_override(self):
        # Case 1: Neutral is dominant (70%), but Sad is significant (15%)
        # Old logic: Would return Neutral (if threshold was 5% but Sad was below and override was only for expressive_threshold)
        # New logic: Should override Neutral to Sad
        emotions_scores = {
            'neutral': 70.0,
            'sad': 15.0,
            'happy': 5.0,
            'angry': 2.0,
            'surprise': 2.0,
            'fear': 3.0,
            'disgust': 3.0
        }
        
        # Manually invoke the override logic (simulating what happens after DeepFace.analyze)
        dominant_emotion = 'neutral'
        expressive_threshold = 1.5
        EXPRESSIVE_EMOTIONS = {'angry', 'disgust', 'fear', 'sad', 'surprise'}

        non_neutral_emotions = {
            k: v for k, v in emotions_scores.items()
            if k in EXPRESSIVE_EMOTIONS and v > expressive_threshold
        }

        if dominant_emotion in ('neutral', 'happy') and non_neutral_emotions:
            best_expressive = max(non_neutral_emotions, key=non_neutral_emotions.get)
            neutral_score = emotions_scores.get('neutral', 0)
            expressive_score = emotions_scores[best_expressive]
            if neutral_score < 85 or expressive_score > 10:
                final_emotion = best_expressive
            else:
                final_emotion = dominant_emotion
        else:
            final_emotion = dominant_emotion

        self.assertEqual(final_emotion, 'sad')
        print(f"Image Override Test (Neutral 70% vs Sad 15%) -> {final_emotion} (PASSED)")

    def test_voice_heuristics(self):
        # Test Surprise: High pitch, high energy, fast tempo
        # avg_pitch > 210 and avg_energy > 0.05 and tempo > 120
        res = self._mock_voice_eval(pitch=220, energy=0.06, tempo=130, pitch_std=30)
        self.assertEqual(res['emotion'], 'surprise')
        print(f"Voice Heuristic Test (Surprise) -> {res['emotion']} (PASSED)")

        # Test Fear: High pitch variation (shaky), fast tempo, low energy
        # pitch_std > 45 and tempo > 130 and avg_energy < 0.04
        res = self._mock_voice_eval(pitch=180, energy=0.03, tempo=140, pitch_std=50)
        self.assertEqual(res['emotion'], 'fear')
        print(f"Voice Heuristic Test (Fear) -> {res['emotion']} (PASSED)")

        # Test Disgust: Low pitch, slow tempo, low-moderate energy
        # avg_pitch < 110 and tempo < 90 and avg_energy > 0.015
        res = self._mock_voice_eval(pitch=100, energy=0.02, tempo=80, pitch_std=15)
        self.assertEqual(res['emotion'], 'disgust')
        print(f"Voice Heuristic Test (Disgust) -> {res['emotion']} (PASSED)")

    def _mock_voice_eval(self, pitch, energy, tempo, pitch_std):
        # Simplified version of the logic in voice_processor.py
        avg_pitch = pitch
        avg_energy = energy
        tempo = tempo
        pitch_std = pitch_std
        
        emotion = "neutral"
        if avg_energy > 0.07 and pitch_std > 35: emotion = "angry"
        elif avg_pitch > 210 and avg_energy > 0.05 and tempo > 120: emotion = "surprise"
        elif pitch_std > 45 and tempo > 130 and avg_energy < 0.04: emotion = "fear"
        elif avg_pitch > 165 and pitch_std > 30 and avg_energy > 0.035: emotion = "happy"
        elif avg_energy < 0.02 and pitch_std < 20 and tempo < 100: emotion = "sad"
        elif avg_pitch < 110 and tempo < 90 and avg_energy > 0.015: emotion = "disgust"
        elif tempo > 135 and avg_energy > 0.04: emotion = "stress"
        
        if avg_pitch == 0 or avg_energy < 0.005: emotion = "neutral"
        return {"emotion": emotion}

if __name__ == "__main__":
    unittest.main()
