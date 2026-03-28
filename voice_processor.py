import librosa
import numpy as np
import soundfile as sf
import io

class VoiceProcessor:
    """
    Analyzes audio features (pitch, pace, energy) to detect emotional states.
    Specifically tuned for stress and sadness detection.
    """
    
    def __init__(self):
        pass

    def analyze_audio(self, audio_bytes):
        """
        Processes audio data to extract emotional features.
        
        Args:
            audio_bytes: Bytes of the audio file (wav/webm)
            
        Returns:
            dict containing detected emotion and confidence
        """
        try:
            # Load audio from bytes
            print(f"VoiceProcessor: Loading {len(audio_bytes)} bytes into librosa...")
            audio_file = io.BytesIO(audio_bytes)
            
            # librosa.load can be picky about formats. 
            # Optimization: Use a lower sampling rate (16k is plenty for sentiment)
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    y, sr = librosa.load(audio_file, sr=16000)
            except Exception as load_err:
                print(f"VoiceProcessor: librosa.load failed: {load_err}")
                # Fallback or more specific info
                raise ValueError(f"Could not decode audio. This is often due to missing 'ffmpeg' on your system for webm files. Error: {load_err}")
            
            import math
            def safe_float(v):
                try:
                    f = float(v)
                    return 0.0 if math.isnan(f) else f
                except:
                    return 0.0

            if len(y) == 0:
                raise ValueError("Audio file is completely empty or silent.")

            # 1. Pitch (F0) Analysis
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            # Filter to human voice range (approx 50Hz to 500Hz) to avoid noise/harmonics
            pitch_values = pitches[(pitches > 50) & (pitches < 500)]
            avg_pitch = safe_float(np.mean(pitch_values)) if len(pitch_values) > 0 else 0.0
            pitch_std = safe_float(np.std(pitch_values)) if len(pitch_values) > 0 else 0.0
            
            # 2. Energy/Volume Analysis (RMS)
            rms = librosa.feature.rms(y=y)
            avg_energy = safe_float(np.mean(rms))
            
            # 3. Pace (Tempo) Analysis
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            # Handle tempo being returned as an array in some librosa versions
            if isinstance(tempo, np.ndarray): tempo = tempo[0] if len(tempo) > 0 else 0.0
            tempo = safe_float(tempo)
            
            # 4. Zero Crossing Rate (Measure of "breathiness" or noise)
            zcr = librosa.feature.zero_crossing_rate(y=y)
            avg_zcr = safe_float(np.mean(zcr))

            # Heuristic Emotion Detection
            emotion = "neutral"
            confidence = 0.6
            
            # Normalize measurements (approximate ranges for speaking voice)
            # Energy typically 0.01 (quiet) to 0.15 (loud)
            # Pitch typically 80 (deep male) to 250 (high female)
            # Pitch std typically 10 (monotone) to 60 (expressive)
            
            # --- EXTENDED VOICE HEURISTICS ---
            
            # 1. Angry: High energy AND high pitch variation (loud and volatile)
            if avg_energy > 0.07 and pitch_std > 35:
                emotion = "angry"
                confidence = 0.85
            
            # 2. Surprise: Sudden high pitch shift, high energy, fast tempo
            elif avg_pitch > 210 and avg_energy > 0.05 and tempo > 120:
                emotion = "surprise"
                confidence = 0.8
            
            # 3. Fear: High pitch variation (shaky), fast tempo, but lower energy (anxious)
            elif pitch_std > 45 and tempo > 130 and avg_energy < 0.04:
                emotion = "fear"
                confidence = 0.75
            
            # 4. Happy: Moderate-high pitch, expressive, moderate energy
            elif avg_pitch > 165 and pitch_std > 30 and avg_energy > 0.035:
                emotion = "happy"
                confidence = 0.75
                
            # 5. Sad: Low energy, low pitch variation, slow tempo (monotone/quiet)
            elif avg_energy < 0.02 and pitch_std < 20 and tempo < 100:
                emotion = "sad"
                confidence = 0.8
                
            # 6. Disgust: Low pitch, slow tempo, low-moderate energy (grumbling)
            elif avg_pitch < 110 and tempo < 90 and avg_energy > 0.015:
                emotion = "disgust"
                confidence = 0.7
                
            # 7. Stress: High tempo, moderate energy, moderate pitch
            elif tempo > 135 and avg_energy > 0.04:
                emotion = "stress"
                confidence = 0.7
            
            # Ensure neutral if nothing is clear
            if avg_pitch == 0 or avg_energy < 0.005:
                emotion = "neutral"
                confidence = 0.5
            
            # Capping confidence
            confidence = min(0.95, confidence)

            return {
                "success": True,
                "emotion": emotion,
                "confidence": round(confidence, 2),
                "features": {
                    "avg_pitch": round(avg_pitch, 2),
                    "tempo": round(tempo, 2),
                    "energy": round(avg_energy, 4)
                }
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }

voice_processor = VoiceProcessor()
