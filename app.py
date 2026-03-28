from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for, flash
from rag_pipeline import MentalHealthChatbot
from mood_detector import MoodDetector
from voice_processor import voice_processor
from wellness_manager import wellness_manager
from mood_tracker import mood_tracker
from auth_manager import auth_manager
from doctor_manager import doctor_manager
from notification_manager import notification_manager
from report_generator import report_generator

import os
import numpy as np
import secrets
import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ── Fast Response Cache (Small Talk) ─────────────────────────────────────────
SMALL_TALK = {
    "hi": "Hello! I'm here and listening. How are you feeling today?",
    "hello": "Hi there! It's good to see you. How's your day going so far?",
    "hey": "Hey! I'm SereneMind. How can I support you right now?",
    "how are you": "I'm doing well, thank you for asking! I'm here to support you. How are *you* doing?",
    "good morning": "Good morning! I hope your day is off to a peaceful start. How are you feeling?",
    "good night": "Good night. I hope you have a restful sleep. Sweet dreams!",
    "thanks": "You're very welcome. I'm always here if you need to talk.",
    "thank you": "It's my pleasure. Take care of yourself!",
}

def get_small_talk(message):
    clean = message.lower().strip().replace("?", "").replace("!", "")
    return SMALL_TALK.get(clean)

# ── Initialization ──────────────────────────────────────────────────────────
bot = MentalHealthChatbot()
mood_detector = MoodDetector()

if not os.path.exists("faiss_index") and os.path.exists("data"):
    print("Pre-ingesting data...")
    bot.ingest_docs()

SLEEP_KEYWORDS = ["sleep", "insomnia", "bedtime", "can't sleep", "nightmare"]

# ── User Routes ──────────────────────────────────────────────────────────────
# ── User Routes ──────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = auth_manager.get_user_by_id(session['user_id'])
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = auth_manager.login_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user.get('role', 'Patient')
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        occupation = request.form.get('occupation')
        role = request.form.get('role', 'Patient')
        
        success, message = auth_manager.register_user(
            username, email, password, full_name, age, gender, occupation, role
        )
        if success:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    image_mood = data.get('image_mood')
    voice_mood = data.get('voice_mood')
    language = data.get('language', 'English')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if wellness_manager.is_crisis(user_message):
        crisis = wellness_manager.get_crisis_response()
        mood_tracker.log_mood("crisis", source="text", trigger_text=user_message)
        return jsonify({"response": None, "crisis": crisis})

    final_mood, confidence = mood_detector.fuse_emotions(image_mood, voice_mood)
    if final_mood and final_mood != "neutral":
        mood_tracker.log_mood(final_mood, confidence=confidence, source="fused", trigger_text=user_message)

    small_talk = get_small_talk(user_message)
    if small_talk:
        return jsonify({"response": small_talk, "fused_mood": "neutral", "wellness": None})

    response = bot.get_response(user_message, mood=final_mood, language=language)
    wellness_plan = None
    if any(sk in user_message.lower() for sk in SLEEP_KEYWORDS):
        wellness_plan = wellness_manager.get_sleep_aid()
    elif final_mood in ("sad", "stress", "angry", "fear", "extreme"):
        wellness_plan = wellness_manager.get_wellness_plan(final_mood)

    return jsonify({"response": response, "fused_mood": final_mood, "confidence": confidence, "wellness": wellness_plan})

@app.route('/api/chat-stream', methods=['POST'])
def chat_stream():
    data = request.json
    user_message = data.get('message', '')
    image_mood = data.get('image_mood')
    voice_mood = data.get('voice_mood')
    language = data.get('language', 'English')
    if not user_message: return jsonify({"error": "No message provided"}), 400

    if wellness_manager.is_crisis(user_message):
        import json
        crisis = wellness_manager.get_crisis_response()
        mood_tracker.log_mood("crisis", source="text", trigger_text=user_message)
        return Response(f"data: {json.dumps({'crisis': crisis})}\n\n", mimetype='text/event-stream')

    small_talk = get_small_talk(user_message)
    if small_talk:
        import json
        return Response(f"data: {json.dumps({'chunk': small_talk, 'fused_mood': 'neutral', 'wellness': None})}\ndata: [DONE]\n\n", mimetype='text/event-stream')

    final_mood, confidence = mood_detector.fuse_emotions(image_mood, voice_mood)
    if final_mood and final_mood != "neutral":
        mood_tracker.log_mood(final_mood, confidence=confidence, source="fused", trigger_text=user_message)
    
    wellness_plan = None
    if final_mood in ("sad", "stress", "angry", "fear"):
        wellness_plan = wellness_manager.get_wellness_plan(final_mood)
    if any(sk in user_message.lower() for sk in SLEEP_KEYWORDS):
        wellness_plan = wellness_manager.get_sleep_aid()

    def generate():
        import json
        yield f"data: {json.dumps({'fused_mood': final_mood, 'confidence': confidence, 'wellness': wellness_plan})}\n\n"
        for chunk in bot.get_response_stream(user_message, mood=final_mood, language=language):
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        yield "data: [DONE]\n\n"
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/detect-mood', methods=['POST'])
def detect_mood():
    try:
        data = request.json
        image_data = data.get('image', '')
        if not image_data: return jsonify({"error": "No image provided"}), 400
        
        print(f"[{datetime.datetime.now()}] Incoming mood detection request...")
        result = mood_detector.detect_emotion(image_data)
        
        if result.get('success'):
            emotion = result['emotion']
            print(f"[{datetime.datetime.now()}] Detected mood: {emotion}")
            result['songs'] = mood_detector.get_song_recommendations(emotion)
            result['wellness'] = wellness_manager.get_wellness_plan(emotion)
            mood_tracker.log_mood(emotion, confidence=result.get('confidence'), source="image")
        else:
            print(f"[{datetime.datetime.now()}] Detection failed: {result.get('message')}")
            
        return jsonify(result)
    except Exception as e:
        print(f"[{datetime.datetime.now()}] CRITICAL ERROR in /api/detect-mood: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": "server_error", "message": str(e)}), 500

@app.route('/api/voice-mood', methods=['POST'])
def voice_mood():
    try:
        if 'audio' not in request.files: return jsonify({"error": "No audio file provided", "success": False}), 400
        audio_file = request.files['audio']
        audio_bytes = audio_file.read()
        result = voice_processor.analyze_audio(audio_bytes)
        if result.get('success'):
            emotion = result['emotion']
            result['songs'] = mood_detector.get_song_recommendations(emotion)
            result['wellness'] = wellness_manager.get_wellness_plan(emotion)
            mood_tracker.log_mood(emotion, confidence=result.get('confidence'), source="voice")
        return jsonify(result)
    except Exception as e:
        print(f"CRITICAL ERROR in /api/voice-mood: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": "server_error", "message": str(e)}), 500


@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    data = request.json
    
    # Standard profile fields
    full_name = data.get('full_name')
    age = data.get('age')
    gender = data.get('gender')
    occupation = data.get('occupation')
    
    # Medical/Emergency fields
    history = data.get('mental_health_history', '')
    em_name = data.get('emergency_contact_name', '')
    em_phone = data.get('emergency_contact_phone', '')
    
    # Update auth_manager (we'll need to expand its update_profile method too)
    auth_manager.update_full_profile(session['user_id'], data)
    return jsonify({"success": True, "message": "Profile updated successfully"})

@app.route('/api/doctors/search', methods=['POST'])
def search_doctors():
    filters = request.json
    doctors = doctor_manager.search_doctors(filters)
    return jsonify({"success": True, "doctors": doctors})

@app.route('/api/hospitals/nearby', methods=['POST'])
def nearby_hospitals():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng') or data.get('lon')
    radius = data.get('radius', 50)
    if lat is None or lng is None:
        return jsonify({"success": False, "error": "Location required"}), 400
    facilities = doctor_manager.get_nearby_facilities(lat, lng, radius)
    return jsonify({"success": True, "facilities": facilities})

@app.route('/api/geocode', methods=['POST'])
def geocode_location():
    """Server-side geocoding using OpenStreetMap Nominatim — no API key required."""
    import urllib.request, urllib.parse, json as json_lib
    data = request.json
    address = (data or {}).get('address', '').strip()
    if not address:
        return jsonify({"success": False, "error": "Address required"}), 400
    
    # Use OpenStreetMap Nominatim — free and no API key needed
    params = urllib.parse.urlencode({'q': address, 'format': 'json', 'limit': 1})
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'MentalHealthChatbot/1.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            results = json_lib.loads(resp.read())
        if results:
            loc = results[0]
            return jsonify({
                "success": True,
                "lat": float(loc['lat']),
                "lng": float(loc['lon']),
                "formatted": loc.get('display_name', address)
            })
        else:
            return jsonify({"success": False, "error": "ZERO_RESULTS"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/appointments/book', methods=['POST'])
def book_appointment():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    data = request.json
    doctor_id = data.get('doctor_id')
    date = data.get('date')
    time = data.get('time')
    session_type = data.get('type', 'Online')
    
    app_id = doctor_manager.book_appointment(doctor_id, session['user_id'], date, time, session_type)
    
    # Schedule notifications (reminders)
    notification_manager.schedule_notifications(app_id, session['user_id'], date, time)
    
    return jsonify({"success": True, "appointment_id": app_id, "message": "Booking request sent to doctor and reminders scheduled!"})

@app.route('/api/appointments/patient', methods=['GET'])
def get_patient_appointments():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    appointments = doctor_manager.get_patient_appointments(session['user_id'])
    return jsonify({"success": True, "appointments": appointments})

@app.route('/api/consultations/report/<int:app_id>', methods=['GET'])
def download_report(app_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    appointment = doctor_manager.get_appointment_by_id(app_id)
    if not appointment or appointment['user_id'] != session['user_id']:
        return jsonify({"success": False, "error": "Appointment not found or unauthorized"}), 404
    
    user = auth_manager.get_user_by_id(session['user_id'])
    
    # Generate PDF in a temporary file
    import tempfile
    from flask import send_file
    
    temp_dir = tempfile.gettempdir()
    report_filename = f"Medical_Report_{app_id}.pdf"
    report_path = os.path.join(temp_dir, report_filename)
    
    report_generator.generate_medical_report(appointment, user, report_path)
    
    return send_file(report_path, as_attachment=True, download_name=report_filename)

@app.route('/api/notifications/pending', methods=['GET'])
def get_pending_notifications():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    # This also acts as a "check" for notifications
    notifications = notification_manager.get_pending_notifications(session['user_id'])
    for notif in notifications:
        # Mark as sent for now - in a real app, this would be handled after actual delivery
        notification_manager.mark_as_sent(notif['id'])
        
    return jsonify({"success": True, "notifications": notifications})





if __name__ == '__main__':
    # threaded=False is required on Windows — DeepFace/TensorFlow are NOT thread-safe
    # and cause hard ntdll.dll crashes when concurrent requests hit the GPU/CPU model.
    # use_reloader=False prevents crashes when models are loaded or files are updated.
    app.run(debug=True, port=5000, threaded=False, use_reloader=False)
