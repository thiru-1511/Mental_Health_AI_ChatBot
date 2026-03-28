# Mental Health AI Chatbot & Consultation Platform 🧠

A comprehensive mental health support application designed to provide users with an empathetic AI chatbot, mood tracking, music therapy features, and a fully integrated doctor booking system for tele-consultations and in-person visits.

## 🌟 Features

* **Empathetic AI Chatbot**: Conversational AI designed to provide emotional support and guidance.
* **Mood Analysis (Voice & Image)**: Analyze the user's emotional state through voice recordings or camera snapshots to provide tailored responses.
* **Music Therapy Integration**: Get dynamic song recommendations based on your current mood and play them directly in the app.
* **Specialist Booking System**: Browse and book appointments with psychiatrists, psychologists, and counselors.
* **Tele-Consultations**: Seamless in-app simulated text, voice, and video calls with doctors.
* **Nearby Help Map**: Interactive map powered by Google Maps & OpenStreetMap Nominatim to find clinics and hospitals near you.
* **Medical History Dashboard**: Keep track of previous consultations, notes, and prescriptions.

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Database**: SQLite
* **Frontend**: HTML, CSS (Custom Glassmorphism Design), Vanilla JavaScript
* **APIs**: 
  * Google Maps API (Map Rendering)
  * OpenStreetMap Nominatim API (Geocoding Location Search)
* **ML/AI Models**: Pre-trained embeddings and classifiers for text and voice mood detection.

## 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thiru-1511/Mental_Health_AI_ChatBot.git
   cd Mental_Health_AI_ChatBot
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you install any missing libraries like `flask`, `sqlite3` etc. required by the backend)*

3. **Set up the Database:**
   The SQLite databases (`doctors.db`, `users.db`, `mood_history.db`) are stored in the `data/` folder and will automatically initialize.

4. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000/`.

## 📂 Project Structure

* `app.py`: Main Flask application server.
* `static/js/script.js`: Core frontend logic, UI interactions, and API fetching.
* `static/css/style.css`: Premium Glassmorphism styling and animations.
* `templates/index.html`: Main application interface.
* `add_more_doctors.py`: Database seeding script to populate doctors.
* `data/`: SQLite database files.

## 🔒 Security Note
*Ensure to restrict your Google Maps API keys to your specific domains if deploying to production.*
