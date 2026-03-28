import base64
import io
import numpy as np
from PIL import Image
from deepface import DeepFace
import cv2
import pandas as pd
import os

class MoodDetector:
    """
    Facial emotion recognition using DeepFace.
    Detects emotions from face images and provides mood analysis.
    """
    
    # Emotion to mood improvement mapping
    MOOD_SUGGESTIONS = {
        'happy': [
            "Great to see you're feeling positive! Keep up the good vibes!",
            "Your happiness is wonderful. Consider sharing it with someone today!",
            "Maintain this positive energy with activities you enjoy."
        ],
        'sad': [
            "I notice you might be feeling down. Would you like to talk about what's on your mind?",
            "It's okay to feel sad sometimes. Consider reaching out to a friend or loved one.",
            "Try engaging in activities that usually bring you comfort, like listening to music or taking a walk.",
            "Remember, these feelings are temporary. Be gentle with yourself."
        ],
        'angry': [
            "I sense some frustration. Taking deep breaths can help calm your mind.",
            "It's valid to feel angry. Consider channeling this energy into physical activity or creative expression.",
            "Try a short meditation or step away from the situation for a moment.",
            "Expressing your feelings in a journal might provide some relief."
        ],
        'fear': [
            "I notice some worry or anxiety. Remember to take things one step at a time.",
            "Fear is a natural response. Try grounding techniques like focusing on your senses.",
            "Consider talking to someone you trust about what's concerning you.",
            "Deep breathing exercises can help manage anxious feelings."
        ],
        'surprise': [
            "You seem surprised! I hope it's something positive.",
            "Unexpected moments can be exciting. Take a moment to process what happened."
        ],
        'neutral': [
            "You seem calm and balanced. How can I support you today?",
            "It's good to be in a neutral, balanced state. What's on your mind?"
        ],
        'disgust': [
            "Something seems to be bothering you. Would you like to talk about it?",
            "It's okay to feel uncomfortable about situations. Let's work through this together."
        ],
        'stress': [
            "I detect some stress in your voice or expression. Take a deep breath with me.",
            "Stress can be overwhelming. Try to focus on one small task at a time.",
            "You've been working hard. Remember to take short breaks to recharge.",
            "Consider a quick 2-minute meditation to lower your cortisol levels."
        ]
    }
    
    # Emotion to song dataset mapping
    MUSIC_DIST = {
        'angry': "data/songs/angry.csv",
        'disgust': "data/songs/disgusted.csv",
        'fear': "data/songs/fearful.csv",
        'happy': "data/songs/happy.csv",
        'neutral': "data/songs/neutral.csv",
        'sad': "data/songs/sad.csv",
        'surprise': "data/songs/surprised.csv"
    }
    
    # AI Curated Song Recommendations - Updated with User Mappings
    AI_CURATED_SONGS = {
        'happy': [ # Energetic
            {"Name": "Happy", "Artist": "Pharrell Williams", "Album": "G I R L"},
            {"Name": "Uptown Funk", "Artist": "Mark Ronson ft. Bruno Mars", "Album": "Uptown Special"},
            {"Name": "Can't Stop the Feeling!", "Artist": "Justin Timberlake", "Album": "Trolls"},
            {"Name": "Shake It Off", "Artist": "Taylor Swift", "Album": "1989"},
            {"Name": "Walking on Sunshine", "Artist": "Katrina and the Waves", "Album": "Walking on Sunshine"},
            {"Name": "Levitating", "Artist": "Dua Lipa", "Album": "Future Nostalgia"}
        ],
        'sad': [ # Calm
            {"Name": "Weightless", "Artist": "Marconi Union", "Album": "Ambient 11"},
            {"Name": "River Flows in You", "Artist": "Yiruma", "Album": "First Love"},
            {"Name": "Clair de Lune", "Artist": "Claude Debussy", "Album": "Suite bergamasque"},
            {"Name": "Fix You", "Artist": "Coldplay", "Album": "X&Y"},
            {"Name": "Gymnopédie No.1", "Artist": "Erik Satie", "Album": "Gymnopédies"},
            {"Name": "Holocene", "Artist": "Bon Iver", "Album": "Bon Iver"}
        ],
        'angry': [ # Relax
            {"Name": "Breathe", "Artist": "Pink Floyd", "Album": "The Dark Side of the Moon"},
            {"Name": "Sunset Lover", "Artist": "Petit Biscuit", "Album": "Presence"},
            {"Name": "Orinoco Flow", "Artist": "Enya", "Album": "Watermark"},
            {"Name": "Teardrop", "Artist": "Massive Attack", "Album": "Mezzanine"},
            {"Name": "Comfortably Numb", "Artist": "Pink Floyd", "Album": "The Wall"},
            {"Name": "Lullaby", "Artist": "Low", "Album": "I Could Live in Hope"}
        ],
        'fear': [ # Comforting & Grounding
            {"Name": "Safe and Sound", "Artist": "Capital Cities", "Album": "In a Tidal Wave of Mystery"},
            {"Name": "Be Okay", "Artist": "Oh Honey", "Album": "With Love"},
            {"Name": "Don't Panic", "Artist": "Coldplay", "Album": "Parachutes"},
            {"Name": "Keep Your Head Up", "Artist": "Andy Grammer", "Album": "Andy Grammer"},
            {"Name": "A Sky Full of Stars", "Artist": "Coldplay", "Album": "Ghost Stories"},
            {"Name": "Count on Me", "Artist": "Bruno Mars", "Album": "Doo-Wops & Hooligans"}
        ],
        'neutral': [ # Focus & Ambient
            {"Name": "Weightless", "Artist": "Marconi Union", "Album": "Ambient 11"},
            {"Name": "LoFi Study Beats", "Artist": "Lofi Girl", "Album": "Chillhop Essentials"},
            {"Name": "Clair de Lune", "Artist": "Claude Debussy", "Album": "Suite bergamasque"},
            {"Name": "Sparks", "Artist": "Coldplay", "Album": "Parachutes"},
            {"Name": "Music for Airports", "Artist": "Brian Eno", "Album": "Ambient 1"},
            {"Name": "Deep Meditation", "Artist": "Peaceful Music", "Album": "Zen"}
        ],
        'surprise': [
            {"Name": "Wow", "Artist": "Post Malone", "Album": "Hollywood's Bleeding"},
            {"Name": "Surprise Surprise", "Artist": "Billy Talent", "Album": "Dead Silence"},
            {"Name": "Uptown Funk", "Artist": "Mark Ronson", "Album": "Uptown Special"}
        ],
        'disgust': [ # Refreshing & Uplifting
            {"Name": "Bad Liar", "Artist": "Imagine Dragons", "Album": "Origins"},
            {"Name": "New Rules", "Artist": "Dua Lipa", "Album": "Dua Lipa"},
            {"Name": "Cleanin' Out My Closet", "Artist": "Eminem", "Album": "The Eminem Show"},
            {"Name": "Stronger", "Artist": "Kanye West", "Album": "Graduation"},
            {"Name": "Good as Hell", "Artist": "Lizzo", "Album": "Cuz I Love You"}
        ],
        'stress': [
            {"Name": "Weightless", "Artist": "Marconi Union", "Album": "Ambient 11"},
            {"Name": "Watermark", "Artist": "Enya", "Album": "Watermark"},
            {"Name": "Strawberry Swing", "Artist": "Coldplay", "Album": "Viva la Vida"}
        ]
    }
    
    def __init__(self, model_name='emotion'):
        """
        Initialize the mood detector parameters.
        Optimized for performance by streamlining the detection pipeline.
        """
        self.model_name = model_name
        self.detector_backend = 'ssd' # Good balance: fast on CPU + accurate for all 7 emotions
        
        # Pre-warm the model to avoid timeouts on the first request
        print("Pre-warming DeepFace model...")
        try:
            # dummy image for warm-up
            dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
            DeepFace.analyze(dummy_img, actions=['emotion'], detector_backend=self.detector_backend, enforce_detection=False, silent=True)
            print("DeepFace model pre-warmed successfully.")
        except Exception as e:
            print(f"Warning: Model pre-warming failed: {e}")
        
    def decode_image(self, base64_string):
        """
        Decode base64 image string to numpy array and resize for speed.
        """
        try:
            # Remove data URL prefix if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64 to bytes
            image_bytes = base64.b64decode(base64_string)
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Performance Optimization: Resize image while maintaining aspect ratio
            # DeepFace works best when the face is not distorted
            max_size = 480  # Larger image = better feature extraction for subtle emotions
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.BICUBIC)
                print(f"Optimized image resize to {new_size} for speed and quality.")
            
            # Convert to numpy array
            img_array = np.array(image)
            
            return img_array
            
        except Exception as e:
            raise ValueError(f"Failed to decode image: {str(e)}")
    
    def detect_emotion(self, base64_image):
        """
        Detect emotion from base64 encoded image.
        
        Args:
            base64_image: Base64 encoded image string
            
        Returns:
            dict with emotion, confidence, and suggestions
        """
        try:
            # Decode image
            img_array = self.decode_image(base64_image)
            
            # Simple brightness check
            avg_brightness = np.mean(img_array)
            if avg_brightness < 20: # Slightly lower threshold, but still dark
                return {
                    'success': False,
                    'error': 'low_light',
                    'message': 'Environment is too dark. Please ensure your face is well-lit for accurate detection.'
                }
            
            # Analyze emotion using DeepFace
            # enforce_detection=True will do the face detection internally
            # Combining detection and analysis in one step is faster
            print(f"Starting optimized DeepFace analysis...")
            result = DeepFace.analyze(
                img_path=img_array,
                actions=['emotion'],
                enforce_detection=True, 
                detector_backend=self.detector_backend,
                silent=True
            )
            print(f"DeepFace analysis complete. Result type: {type(result)}")
            
            # Handle both single face and multiple faces
            if isinstance(result, list):
                result = result[0]
            
            # Get dominant emotion
            emotions_scores = result['emotion']
            dominant_emotion = result['dominant_emotion']
            
            # --- EMOTION SENSITIVITY FIX ---
            # The model can be biased toward 'neutral' or 'happy'.
            # If ANY expressive emotion scores above the threshold, prefer it over neutral/happy.
            # Lowered threshold to 1.5% to catch subtle expressions (sad, fearful, disgusted, angry, surprised).
            expressive_threshold = 1.5
            EXPRESSIVE_EMOTIONS = {'angry', 'disgust', 'fear', 'sad', 'surprise'}

            non_neutral_emotions = {
                k: v for k, v in emotions_scores.items()
                if k in EXPRESSIVE_EMOTIONS and v > expressive_threshold
            }

            if dominant_emotion in ('neutral', 'happy') and non_neutral_emotions:
                # Prefer the strongest expressive emotion over neutral/happy bias
                # Sort by score to find the best expressive emotion
                best_expressive = max(non_neutral_emotions, key=non_neutral_emotions.get)
                
                # If neutral is dominant but not "massively" dominant (e.g., less than 85%),
                # or if the expressive emotion is significant (> 10%), override it.
                neutral_score = emotions_scores.get('neutral', 0)
                expressive_score = emotions_scores[best_expressive]
                
                if neutral_score < 85 or expressive_score > 10:
                    print(f"Overriding '{dominant_emotion}' ({emotions_scores[dominant_emotion]:.1f}%) "
                          f"→ '{best_expressive}' ({emotions_scores[best_expressive]:.1f}%)")
                    emotion = best_expressive
                    confidence = emotions_scores[best_expressive]
                else:
                    emotion = dominant_emotion
                    confidence = emotions_scores[emotion]
            else:
                emotion = dominant_emotion
                confidence = emotions_scores[emotion]
            
            # Debug log for terminal
            print(f"Final Detection: {emotion} | Raw Scores: {emotions_scores}")
            
            # Convert numpy types to Python native types for JSON serialization
            emotions_scores_serializable = {k: float(v) for k, v in emotions_scores.items()}
            
            # Get mood improvement suggestions
            suggestions = self.MOOD_SUGGESTIONS.get(emotion, [
                "I'm here to support you. How are you feeling?"
            ])
            
            return {
                'success': True,
                'emotion': emotion,
                'confidence': round(float(confidence), 2),
                'all_emotions': emotions_scores_serializable,
                'suggestions': suggestions,
                'message': f"Detected emotion: {emotion.capitalize()} ({float(confidence):.1f}% confidence)"
            }
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # DeepFace raises ValueError for face detection failure
            if 'face could not be detected' in error_msg or 'no face' in error_msg:
                return {
                    'success': False,
                    'error': 'no_face_detected',
                    'message': 'No face detected in the image. Please ensure your face is clearly visible and well-lit.'
                }
            elif 'multiple faces' in error_msg:
                return {
                    'success': False,
                    'error': 'multiple_faces',
                    'message': 'Multiple faces detected. Please ensure only your face is in the frame.'
                }
            else:
                return {
                    'success': False,
                    'error': 'analysis_error',
                    'message': f'Error analyzing image: {str(e)}'
                }
    
    def get_song_recommendations(self, emotion):
        """
        Get song recommendations based on detected emotion.
        Combines AI-curated songs with random samples from the dataset for variety.
        
        Args:
            emotion: Detected emotion string
            
        Returns:
            list of dicts containing song Name, Album, and Artist
        """
        try:
            # 1. Start with AI-curated songs for quality
            recommendations = self.AI_CURATED_SONGS.get(emotion, []).copy()
            
            # 2. Add songs from CSV dataset if available
            csv_path = self.MUSIC_DIST.get(emotion)
            if csv_path and os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                required_cols = ['Name', 'Album', 'Artist']
                if all(col in df.columns for col in required_cols):
                    # Take up to 50 random songs from dataset for high variety
                    dataset_songs = df[required_cols].sample(min(50, len(df))).to_dict(orient='records')
                    recommendations.extend(dataset_songs)
            
            # 3. Use pandas to drop duplicates and shuffle
            if recommendations:
                temp_df = pd.DataFrame(recommendations).drop_duplicates(subset=['Name', 'Artist'])
                # Shuffle the results and take top 20
                results = temp_df.sample(min(20, len(temp_df))).to_dict(orient='records')
                
                # Add YouTube Search URL (Fast, no network request)
                for song in results:
                    search_query = f"{song['Name']} {song['Artist']} official".replace(" ", "+")
                    song['url'] = f"https://www.youtube.com/results?search_query={search_query}"
                
                return results
                
            return recommendations
            
        except Exception as e:
            print(f"Error getting song recommendations: {e}")
            fallback = self.AI_CURATED_SONGS.get(emotion, [])[:4]
            for song in fallback:
                query = f"{song['Name']} {song['Artist']} official".replace(" ", "+")
                song['url'] = f"https://www.youtube.com/results?search_query={query}"
            return fallback
    
    def get_mood_context_prompt(self, emotion, user_message):
        """
        Generate a context-aware prompt for the chatbot based on detected mood.
        
        Args:
            emotion: Detected emotion
            user_message: User's text message
            
        Returns:
            Enhanced prompt with mood context
        """
        mood_context = {
            'happy': "The user appears to be in a positive mood.",
            'sad': "The user appears to be feeling sad or down. Be empathetic and supportive.",
            'angry': "The user appears to be frustrated or angry. Be calm and understanding.",
            'fear': "The user appears to be anxious or worried. Be reassuring and gentle.",
            'neutral': "The user appears to be in a neutral, calm state.",
            'surprise': "The user appears to be surprised.",
            'disgust': "The user appears to be uncomfortable or bothered by something."
        }
        
        context = mood_context.get(emotion, "")
        
        return f"{context}\n\nUser's message: {user_message}\n\nProvide an empathetic, supportive response that acknowledges their emotional state."

    def fuse_emotions(self, text_mood=None, image_mood=None, voice_mood=None):
        """
        Combines emotions from different modalities (Late Fusion).
        
        Weights:
        - Image: 0.4 (Facial micro-expressions are very reliable)
        - Voice: 0.35 (Tone/Pitch adds deep context)
        - Text: 0.25 (Verbal content)
        """
        modalities = []
        if text_mood: modalities.append(('text', text_mood, 0.25))
        if image_mood: modalities.append(('image', image_mood, 0.40))
        if voice_mood: modalities.append(('voice', voice_mood, 0.35))
        
        if not modalities:
            return "neutral", 1.0
            
        # If only one, return it
        if len(modalities) == 1:
            return modalities[0][1], 1.0
            
        # Simplified weighted voting
        scores = {}
        for mod_type, emotion, weight in modalities:
            scores[emotion] = scores.get(emotion, 0) + weight
            
        # Get dominant emotion from fusion
        fused_emotion = max(scores, key=scores.get)
        confidence = scores[fused_emotion]
        
        return fused_emotion, round(float(confidence), 2)
