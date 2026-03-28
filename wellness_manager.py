
"""
Wellness Manager — curated breathing exercises, meditations, and podcasts
for each detected emotion. Also handles crisis escalation detection.
"""

import random
from datetime import datetime, date


# ──────────────────────────────────────────────────────────────────────────────
# Crisis Keywords (kept in one place for easy updating)
# ──────────────────────────────────────────────────────────────────────────────
CRISIS_KEYWORDS = [
    "want to die", "kill myself", "end my life", "suicide", "suicidal",
    "no reason to live", "give up on life", "can't go on", "worthless",
    "hopeless", "no point anymore", "self harm", "hurt myself",
    "don't want to be here", "make it stop", "nothing matters"
]

# ──────────────────────────────────────────────────────────────────────────────
# Wellness Content Library
# ──────────────────────────────────────────────────────────────────────────────
WELLNESS_CONTENT = {
    "sad": {
        "breathing": [
            {
                "title": "4-7-8 Calming Breath",
                "description": "Inhale for 4 seconds, hold for 7, exhale for 8. Repeat 4 times. This activates your parasympathetic nervous system.",
                "duration": "2 min",
                "icon": "🌬️"
            },
            {
                "title": "Box Breathing",
                "description": "Inhale 4 sec → Hold 4 sec → Exhale 4 sec → Hold 4 sec. Visualise drawing a box as you breathe.",
                "duration": "3 min",
                "icon": "📦"
            }
        ],
        "meditations": [
            {
                "title": "Self-Compassion Meditation",
                "description": "A gentle 5-minute practice to remind yourself it's okay to feel sad.",
                "link": "https://www.youtube.com/results?search_query=self+compassion+meditation+5+minutes",
                "icon": "🧘"
            },
            {
                "title": "Loving-Kindness (Metta)",
                "description": "Cultivate warmth and kindness towards yourself first, then others.",
                "link": "https://www.youtube.com/results?search_query=loving+kindness+meditation+guided",
                "icon": "💗"
            }
        ],
        "podcasts": [
            {"title": "The Happiness Lab", "host": "Dr. Laurie Santos", "topic": "Science-backed ways to feel better"},
            {"title": "Therapy Chat", "host": "Laura Reagan, LCSW-C", "topic": "Mental wellness conversations"}
        ]
    },
    "stress": {
        "breathing": [
            {
                "title": "Physiological Sigh",
                "description": "Take a double inhale through the nose (sniff, sniff), then one long slow exhale. The fastest way to reduce acute stress.",
                "duration": "30 sec",
                "icon": "😮‍💨"
            },
            {
                "title": "Diaphragmatic Breathing",
                "description": "Place one hand on your chest, one on your belly. Breathe so only the belly hand moves. 6 breaths per minute.",
                "duration": "2 min",
                "icon": "🫁"
            }
        ],
        "meditations": [
            {
                "title": "Body Scan for Stress Release",
                "description": "Slowly scan from head to toe, consciously releasing tension in each muscle group.",
                "link": "https://www.youtube.com/results?search_query=body+scan+meditation+stress+relief",
                "icon": "🦾"
            },
            {
                "title": "NSDR (Non-Sleep Deep Rest)",
                "description": "A 10-minute protocol proven to restore focus and calm the nervous system.",
                "link": "https://www.youtube.com/results?search_query=NSDR+10+minutes+Andrew+Huberman",
                "icon": "🌊"
            }
        ],
        "podcasts": [
            {"title": "The Mindful Kind", "host": "Rachael Kable", "topic": "Practical mindfulness for busy people"},
            {"title": "Calm Masterclass", "host": "Calm App", "topic": "Daily meditations and stress reduction"}
        ]
    },
    "angry": {
        "breathing": [
            {
                "title": "Cooling Breath (Sitali)",
                "description": "Curl your tongue into a tube, inhale through it slowly, hold, then exhale through the nose. Instantly cools body and mind.",
                "duration": "2 min",
                "icon": "❄️"
            },
            {
                "title": "Extended Exhale",
                "description": "Inhale for 4 seconds, exhale for 8 seconds. The longer exhale dominates the parasympathetic response.",
                "duration": "2 min",
                "icon": "🌬️"
            }
        ],
        "meditations": [
            {
                "title": "Anger Release Meditation",
                "description": "Acknowledge and safely process your anger through guided visualization.",
                "link": "https://www.youtube.com/results?search_query=guided+meditation+anger+release",
                "icon": "🔥"
            }
        ],
        "podcasts": [
            {"title": "Unlocking Us", "host": "Brené Brown", "topic": "Shame, anger and human courage"},
        ]
    },
    "fear": {
        "breathing": [
            {
                "title": "5-5-5 Grounding Breath",
                "description": "Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste. Then breathe deeply 5 times.",
                "duration": "3 min",
                "icon": "🌿"
            }
        ],
        "meditations": [
            {
                "title": "Grounding Meditation",
                "description": "Feel the earth beneath you. A powerful tool for anxiety and fear.",
                "link": "https://www.youtube.com/results?search_query=grounding+meditation+anxiety+relief",
                "icon": "🌱"
            }
        ],
        "podcasts": [
            {"title": "Feel Better, Live More", "host": "Dr. Rangan Chatterjee", "topic": "Anxiety reduction and resilience"}
        ]
    },
    "happy": {
        "breathing": [
            {
                "title": "Energising Breath",
                "description": "Quick rhythmic inhales and exhales through the nose for 30 seconds (Kapalbhati). Amplifies positive energy!",
                "duration": "1 min",
                "icon": "⚡"
            }
        ],
        "meditations": [
            {
                "title": "Gratitude Meditation",
                "description": "Amplify your happiness by meditating on what you are grateful for right now.",
                "link": "https://www.youtube.com/results?search_query=gratitude+meditation+5+minutes",
                "icon": "🙏"
            }
        ],
        "podcasts": [
            {"title": "The Positive Psychology Podcast", "host": "Kristen Truempy", "topic": "Flourishing and well-being"}
        ]
    },
    "neutral": {
        "breathing": [
            {
                "title": "Coherence Breathing",
                "description": "Inhale for 5 seconds, exhale for 5 seconds. Synchronises heart rate and breath for optimal mental clarity.",
                "duration": "3 min",
                "icon": "🎯"
            }
        ],
        "meditations": [
            {
                "title": "Mindfulness of the Present",
                "description": "A simple 5-minute sit, noticing thoughts without judgment.",
                "link": "https://www.youtube.com/results?search_query=5+minute+mindfulness+meditation",
                "icon": "🧠"
            }
        ],
        "podcasts": [
            {"title": "Ten Percent Happier", "host": "Dan Harris", "topic": "Meditation for skeptics"}
        ]
    },
    "disgust": {
        "breathing": [
            {
                "title": "Clearance Breath",
                "description": "Inhale deeply, then exhale with a forceful 'ha' sound to release the feeling of discomfort.",
                "duration": "1 min",
                "icon": "✨"
            }
        ],
        "meditations": [
            {
                "title": "Mindful Acceptance",
                "description": "Observe the feeling of disgust without judgment and let it pass like a cloud.",
                "link": "https://www.youtube.com/results?search_query=mindful+acceptance+meditation",
                "icon": "☁️"
            }
        ],
        "podcasts": [
            {"title": "The Science of Disgust", "host": "Stuff You Should Know", "topic": "Understanding this complex emotion"}
        ]
    },
    "surprise": {
        "breathing": [
            {
                "title": "Centering Breath",
                "description": "Slow, deep inhales to bring your heart rate back to a steady rhythm after a surprise.",
                "duration": "2 min",
                "icon": "⚖️"
            }
        ],
        "meditations": [
            {
                "title": "Staying Present",
                "description": "Ground yourself in the 'now' after an unexpected event.",
                "link": "https://www.youtube.com/results?search_query=staying+present+meditation",
                "icon": "🧘"
            }
        ],
        "podcasts": [
            {"title": "The Power of Surprise", "host": "Tania Luna", "topic": "How to embrace the unexpected"}
        ]
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# Music Therapy Playlists
# ──────────────────────────────────────────────────────────────────────────────
PLAYLISTS = {
    "calm": [
        {"title": "Deep Focus & Calm", "url": "https://open.spotify.com/playlist/37i9dQZF1DWZeKzbUnY3Y9"},
        {"title": "Liquid Mind Relaxation", "url": "https://www.youtube.com/watch?v=17XmFTK4I-s"}
    ],
    "uplifting": [
        {"title": "Feel Good Indie", "url": "https://open.spotify.com/playlist/37i9dQZF1DWZ77pCdfFf19"},
        {"title": "Uplifting Classics", "url": "https://www.youtube.com/watch?v=vPhgM862Atw"}
    ],
    "focus": [
        {"title": "Lofi Beats for Focus", "url": "https://www.youtube.com/watch?v=jfKfPfyJRdk"},
        {"title": "Alpha Waves concentration", "url": "https://open.spotify.com/playlist/37i9dQZF1DX60s9v6o9up0"}
    ],
    "sleep": [
        {"title": "Deep Sleep Melodies", "url": "https://open.spotify.com/playlist/37i9dQZF1DWZd79jYcmmUu"},
        {"title": "Gentle Rainfall (10 Hours)", "url": "https://www.youtube.com/watch?v=mPZkdNFkNps"}
    ]
}

# ──────────────────────────────────────────────────────────────────────────────
# Environment & Activity Suggestions
# ──────────────────────────────────────────────────────────────────────────────
ENVIRONMENT_ACTIVITIES = {
    "high_stress": ["Take a cold shower to reset your nervous system.", "Go for a 10-minute walk without your phone.", "Try journaling for 5 minutes."],
    "low_energy": ["Stretch your body for 2 minutes.", "Drink a glass of water.", "Stand in direct sunlight if possible."],
    "anxious": ["Organize one small space (like a drawer).", "Color a simple pattern.", "Step outside and name 3 things you can see."],
    "default": ["Take a moment to check your posture.", "Practice a quick gratitude check-in.", "Listen to your favorite song."]
}

# Default fallbacks (removed as we added specific content)


class WellnessManager:
    """
    Provides personalised wellness recommendations (breathing, meditation, podcasts)
    and crisis escalation detection.
    """

    def get_wellness_plan(self, emotion: str) -> dict:
        """
        Returns a wellness plan for the given emotion, including music and activities.
        """
        content = WELLNESS_CONTENT.get(emotion, WELLNESS_CONTENT["neutral"])
        plan = {}

        # 1. Breathing, Meditations, Podcasts
        if content.get("breathing"):
            plan["breathing"] = random.choice(content["breathing"])
        if content.get("meditations"):
            plan["meditation"] = random.choice(content["meditations"])
        if content.get("podcasts"):
            plan["podcast"] = random.choice(content["podcasts"])

        # 2. Music Therapy Playlist
        mood_to_music = {
            "sad": "uplifting",
            "stress": "calm",
            "angry": "calm",
            "fear": "calm",
            "neutral": "focus",
            "happy": "uplifting"
        }
        playlist_type = mood_to_music.get(emotion, "calm")
        plan["playlist"] = random.choice(PLAYLISTS[playlist_type])

        # 3. Activity Suggestion
        if emotion in ("stress", "angry"):
            plan["activity"] = random.choice(ENVIRONMENT_ACTIVITIES["high_stress"])
        elif emotion == "sad":
             plan["activity"] = random.choice(ENVIRONMENT_ACTIVITIES["low_energy"])
        elif emotion == "fear":
             plan["activity"] = random.choice(ENVIRONMENT_ACTIVITIES["anxious"])
        else:
             plan["activity"] = random.choice(ENVIRONMENT_ACTIVITIES["default"])

        return plan

    def get_sleep_aid(self):
        """Returns sleep-focused calming content."""
        return {
            "playlist": random.choice(PLAYLISTS["sleep"]),
            "activity": "Try a digital detox (no phones) 30 minutes before bed.",
            "prompt": "I can tell you a calming bedtime story. Just ask: 'Tell me a sleep story'."
        }

    def is_crisis(self, text: str) -> bool:
        """
        Checks whether a user message contains crisis-level distress signals.
        """
        text_lower = text.lower()
        return any(kw in text_lower for kw in CRISIS_KEYWORDS)

    def get_crisis_response(self) -> dict:
        """
        Returns a safe, compassionate crisis escalation response.
        """
        return {
            "is_crisis": True,
            "message": (
                "I hear you, and I'm really glad you reached out. 💙\n\n"
                "What you're feeling is serious, and you deserve real support right now.\n\n"
                "Please reach out to someone who can help:"
            ),
            "resources": [
                {"name": "iCall (India)", "number": "9152987821", "url": "https://icallhelpline.org/"},
                {"name": "Vandrevala Foundation", "number": "1860-2662-345", "url": "https://www.vandrevalafoundation.com/"},
                {"name": "iMind (Bangalore)", "number": "080-46110007", "url": "https://nimhans.ac.in/"},
                {"name": "Crisis Text Line (Global)", "number": "Text HOME to 741741", "url": "https://www.crisistextline.org/"}
            ],
            "reminder": "You are not alone. Things can and do get better. 🌱"
        }


wellness_manager = WellnessManager()
