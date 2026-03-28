document.addEventListener('DOMContentLoaded', () => {

    // ── DOM References ────────────────────────────────────────────────────────
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesContainer = document.getElementById('messages-container');
    const typingIndicator = document.getElementById('typing-indicator');

    // Camera
    const cameraBtn = document.getElementById('camera-btn');
    const cameraModal = document.getElementById('camera-modal');
    const closeCameraBtn = document.getElementById('close-camera');
    const cameraFeed = document.getElementById('camera-feed');
    const captureBtn = document.getElementById('capture-btn');
    const capturedImage = document.getElementById('captured-image');
    const postCaptureControls = document.getElementById('post-capture-controls');
    const retakeBtn = document.getElementById('retake-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const snapshotCanvas = document.getElementById('snapshot-canvas');
    const moodResult = document.getElementById('mood-result');
    const moodBadge = document.getElementById('mood-badge');
    const moodText = document.getElementById('mood-text');
    const clearMoodBtn = document.getElementById('clear-mood');
    const detectionStatus = document.getElementById('detection-status');
    const cameraGuide = document.getElementById('camera-guide');
    const cameraFlash = document.getElementById('camera-flash');

    // Voice
    const micBtn = document.getElementById('mic-btn');
    const voiceOverlay = document.getElementById('voice-overlay');
    const stopMicBtn = document.getElementById('stop-mic');

    // Voice Controller
    const dictateBtn = document.getElementById('dictate-btn');
    const ttsToggleBtn = document.getElementById('tts-toggle');
    const ttsIcon = document.getElementById('tts-icon');
    const ttsText = document.getElementById('tts-text');
    let isTtsEnabled = false;

    // Crisis
    const crisisOverlay = document.getElementById('crisis-overlay');
    const crisisMessage = document.getElementById('crisis-message');
    const crisisResources = document.getElementById('crisis-resources');
    const crisisReminder = document.getElementById('crisis-reminder');
    const closeCrisisBtn = document.getElementById('close-crisis');

    // Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');

    // Timer
    const timerBtn = document.getElementById('timer-btn');
    const timerModal = document.getElementById('timer-modal');
    const closeTimerBtn = document.getElementById('close-timer');
    const breathingCircle = document.getElementById('breathing-circle');
    const breathingText = document.getElementById('breathing-text');
    const countdownTimer = document.getElementById('countdown-timer');
    const startTimerBtn = document.getElementById('start-timer');

    // Profile
    const profileForm = document.getElementById('profile-form');
    const profileBio = document.getElementById('profile-bio');
    const profileName = document.getElementById('profile-name');
    const profileAge = document.getElementById('profile-age');
    const profileGender = document.getElementById('profile-gender');
    const profileHistory = document.getElementById('profile-history');
    const profileEmName = document.getElementById('profile-em-name');
    const profileEmPhone = document.getElementById('profile-em-phone');

    // Healthcare / Specialists
    const doctorListSimple = document.getElementById('doctor-list-simple');
    const bookingModalSimple = document.getElementById('booking-modal-simple');
    const closeBookingSimple = document.getElementById('close-booking-simple');
    const bookingDrName = document.getElementById('booking-dr-name');
    const bookDate = document.getElementById('book-date');
    const bookTime = document.getElementById('book-time');
    const bookType = document.getElementById('book-type');
    const nextToPayment = document.getElementById('next-to-payment');
    const confirmPaymentSim = document.getElementById('confirm-payment-sim');
    const confirmWhatsapp = document.getElementById('confirm-whatsapp');

    const bookingStep1 = document.getElementById('booking-step-1');
    const bookingStep2 = document.getElementById('booking-step-2');
    const bookingStep3 = document.getElementById('booking-step-3');

    // Consultation System
    const consultationList = document.getElementById('consultation-list');
    const consultationModal = document.getElementById('consultation-modal');
    const closeConsultation = document.getElementById('close-consultation');
    const consultationMedia = document.getElementById('consultation-media');
    const consultationChat = document.getElementById('consultation-chat');
    const chatDrName = document.getElementById('chat-dr-name');
    const consultationMessages = document.getElementById('consultation-messages');
    const consultationInput = document.getElementById('consultation-input');
    const sendConsultationBtn = document.getElementById('send-consultation-btn');
    const endCallBtn = document.getElementById('end-call-btn');
    const consultationVideoRemote = document.getElementById('consultation-video-remote');
    const consultationVideoLocal = document.getElementById('consultation-video-local');
    const consultationStatus = document.getElementById('consultation-status');
    const toggleMicBtn = document.getElementById('toggle-mic-btn');
    const toggleVideoBtn = document.getElementById('toggle-video-btn');

    let selectedDoctor = null;
    const findDoctorBtn = null; // Removed from UI

    // Music Player
    const musicModal = document.getElementById('music-modal');
    const closeMusicBtn = document.getElementById('close-music');
    const backToResultsBtn = document.getElementById('back-to-results');
    const nowPlayingTitle = document.getElementById('now-playing-title');
    const songDetailText = document.getElementById('song-detail-text');

    // Selectors
    const langSelect = document.getElementById('lang-select');

    let currentDays = 7;
    let cameraStream = null;

    // ── Missing Functions Stubs ──────────────────────────────────────────────

    // ── State Variables ──────────────────────────────────────────────────────
    let detectedImageMood = null;
    let detectedVoiceMood = null;
    let mediaRecorder = null;
    let audioChunks = [];
    let moodChartInst = null;
    let pieChartInst = null;

    // Daily quotes pool
    const QUOTES = [
        { text: "The journey of a thousand miles begins with a single step.", author: "Lao Tzu" },
        { text: "You don't have to control your thoughts; you just have to stop letting them control you.", author: "Dan Millman" },
        { text: "Nothing can bring you peace but yourself.", author: "Ralph Waldo Emerson" },
        { text: "Every moment is a fresh beginning.", author: "T.S. Eliot" },
        { text: "Be the change you wish to see in the world.", author: "Mahatma Gandhi" },
        { text: "The present moment always will have been.", author: "Eckhart Tolle" },
        { text: "You are enough, a thousand times enough.", author: "Atticus" },
        { text: "Storms make trees take deeper roots.", author: "Dolly Parton" }
    ];

    // ── Core Event Listeners ─────────────────────────────────────────────────
    if (sendBtn) sendBtn.onclick = sendMessage;
    if (userInput) {
        userInput.onkeydown = (e) => { if (e.key === 'Enter') sendMessage(); };
    }
    if (cameraBtn) cameraBtn.onclick = startCamera;
    if (captureBtn) captureBtn.onclick = captureFace;
    if (retakeBtn) retakeBtn.onclick = retakeSnapshot;
    if (analyzeBtn) analyzeBtn.onclick = analyzeSnapshot;
    if (micBtn) micBtn.onclick = startVoiceRecording;
    if (stopMicBtn) stopMicBtn.onclick = stopVoiceRecording;
    if (closeCameraBtn) closeCameraBtn.onclick = stopCamera;
    if (clearMoodBtn) clearMoodBtn.onclick = clearMood;
    if (timerBtn) timerBtn.onclick = openTimer;
    if (closeTimerBtn) closeTimerBtn.onclick = closeTimer;
    if (startTimerBtn) startTimerBtn.onclick = startTimer;

    // ── Tab Routing ───────────────────────────────────────────────────────────
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            document.querySelectorAll('.tab-content').forEach(el => {
                el.style.display = 'none';
                el.classList.remove('active');
            });

            const target = document.getElementById(`tab-${tab}`);
            if (target) {
                target.style.display = 'flex';
                target.classList.add('active');

                // Specific tab logic
                if (tab === 'healthcare') {
                    if (typeof loadSpecialists === 'function') {
                        loadSpecialists();
                    }
                } else if (tab === 'consultations') {
                    loadConsultations();
                } else if (tab === 'history') {
                    loadHistory();
                }
            }
        });
    });


    // ── Music Player Modal Logic ──────────────────────────────────────────
    // Event Delegation for Song Cards
    document.addEventListener('click', (e) => {
        const card = e.target.closest('.song-card');
        if (card && card.dataset.url) {
            window.playSong(card.dataset.url, card.dataset.name, card.dataset.artist);
        }
    });

    window.playSong = function (url, name, artist) {
        const query = encodeURIComponent(name + ' ' + artist);
        const ytSearchUrl = `https://www.youtube.com/results?search_query=${query}`;
        const spSearchUrl = `https://open.spotify.com/search/${query}`;

        // Also update the modal for info display
        if (nowPlayingTitle) nowPlayingTitle.textContent = `Now Playing: ${name}`;
        if (songDetailText) songDetailText.textContent = `${artist} – Select your platform!`;

        // Hide the broken iframe, show headphones icon instead
        const musicVideoContainer = document.getElementById('music-video-container');
        const musicIframe = document.getElementById('music-iframe');
        const headphonesIcon = document.getElementById('headphones-icon');
        if (musicVideoContainer) musicVideoContainer.style.display = 'none';
        if (musicIframe) musicIframe.src = '';
        if (headphonesIcon) headphonesIcon.style.display = 'block';

        // Update external links
        const ytLink = document.getElementById('link-youtube');
        const spLink = document.getElementById('link-spotify');
        if (ytLink) ytLink.href = ytSearchUrl;
        if (spLink) spLink.href = spSearchUrl;

        // Show the modal as a confirmation
        if (musicModal) musicModal.classList.add('active');
    };

    if (closeMusicBtn) {
        closeMusicBtn.onclick = () => {
            const musicIframe = document.getElementById('music-iframe');
            if (musicIframe) musicIframe.src = ""; // Stop playback on close
            musicModal.classList.remove('active');
        };
    }

    if (backToResultsBtn) {
        backToResultsBtn.onclick = () => {
            const musicIframe = document.getElementById('music-iframe');
            if (musicIframe) musicIframe.src = ""; // Stop playback
            musicModal.classList.remove('active');
        };
    }

    // ── Messages ──────────────────────────────────────────────────────────────
    function appendMessage(html, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.innerHTML = sender === 'user'
            ? '<i class="fa-solid fa-user"></i>'
            : '<i class="fa-solid fa-robot"></i>';

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.innerHTML = (sender === 'user')
            ? html.replace(/\n/g, '<br>')
            : html;

        if (sender === 'user') {
            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(avatarDiv);
        } else {
            messageDiv.appendChild(avatarDiv);
            messageDiv.appendChild(contentDiv);
        }

        messagesContainer.appendChild(messageDiv);
        scrollToBottom();
        return messageDiv;
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function showTyping() { typingIndicator.style.display = 'flex'; scrollToBottom(); }
    function hideTyping() { typingIndicator.style.display = 'none'; }

    // ── Wellness Panel Builder ────────────────────────────────────────────────
    function buildWellnessPanel(wellness) {
        if (!wellness) return '';
        let html = '<div class="wellness-panel"><h4>🌿 Wellness Recommendations</h4>';

        // 1. Activity Suggestion (Environment)
        if (wellness.activity) {
            html += `<div class="wellness-item">
                <div class="wellness-item-icon">✨</div>
                <div>
                    <div class="wellness-item-title">Suggested Activity</div>
                    <div class="wellness-item-desc">${wellness.activity}</div>
                </div>
            </div>`;
        }

        // 2. Music Therapy Playlist
        if (wellness.playlist) {
            html += `<div class="wellness-item">
                <div class="wellness-item-icon">🎵</div>
                <div>
                    <div class="wellness-item-title">${wellness.playlist.title}</div>
                    <div class="wellness-item-desc">Recommended for your current mood.</div>
                    <a class="wellness-item-link" href="${wellness.playlist.url}" target="_blank">▶ Open Playlist</a>
                </div>
            </div>`;
        }

        if (wellness.breathing) {
            html += `<div class="wellness-item">
                <div class="wellness-item-icon">${wellness.breathing.icon}</div>
                <div>
                    <div class="wellness-item-title">${wellness.breathing.title} <span style="color:#64748b;font-size:0.75rem;">(${wellness.breathing.duration})</span></div>
                    <div class="wellness-item-desc">${wellness.breathing.description}</div>
                </div>
            </div>`;
        }

        if (wellness.meditation) {
            html += `<div class="wellness-item">
                <div class="wellness-item-icon">${wellness.meditation.icon}</div>
                <div>
                    <div class="wellness-item-title">${wellness.meditation.title}</div>
                    <div class="wellness-item-desc">${wellness.meditation.description}</div>
                    <a class="wellness-item-link" href="${wellness.meditation.link}" target="_blank">▶ Open guided session</a>
                </div>
            </div>`;
        }

        if (wellness.podcast) {
            html += `<div class="wellness-item">
                <div class="wellness-item-icon">🎙️</div>
                <div>
                    <div class="wellness-item-title">${wellness.podcast.title}</div>
                    <div class="wellness-item-desc">${wellness.podcast.topic} · by ${wellness.podcast.host}</div>
                </div>
            </div>`;
        }

        // 3. Prompt for Story
        if (wellness.prompt) {
            html += `<p style="font-size:0.8rem;color:#94a3b8;margin-top:10px;font-style:italic;">${wellness.prompt}</p>`;
        }

        html += '</div>';
        return html;
    }

    // ── Chat / Send Message ───────────────────────────────────────────────────
    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // ── Small Talk Quick Response ───────────────────────────────────────
        const quickResponses = {
            "hi": "Hello! I'm here and listening. How are you feeling today?",
            "hello": "Hi there! It's good to see you. How's your day going so far?",
            "hey": "Hey! I'm SereneMind. How can I support you right now?",
            "how are you": "I'm doing well, thank you for asking! I'm here to support you. How are *you* doing?",
            "good morning": "Good morning! I hope your day is off to a peaceful start. How are you feeling?",
            "good night": "Good night. I hope you have a restful sleep. Sweet dreams!",
            "thanks": "You're very welcome. I'm always here if you need to talk.",
            "thank you": "It's my pleasure. Take care of yourself!"
        };
        const cleanText = text.toLowerCase().replace(/[?!]/g, "").trim();
        if (quickResponses[cleanText]) {
            userInput.value = '';
            appendMessage(text, 'user');
            appendMessage(quickResponses[cleanText], 'bot');
            return;
        }

        userInput.value = '';
        appendMessage(text, 'user');
        showTyping();

        try {
            const payload = {
                message: text,
                language: langSelect ? langSelect.value : 'English',
                image_mood: detectedImageMood || null,
                voice_mood: detectedVoiceMood || null
            };

            const resp = await fetch('/api/chat-stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!resp.ok) throw new Error('Network response was not ok');

            const reader = resp.body.getReader();
            const decoder = new TextDecoder();
            let botMessageDiv = null;
            let botContentEl = null;
            let fullText = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.replace('data: ', '');
                        if (dataStr === '[DONE]') break;

                        try {
                            const data = JSON.parse(dataStr);

                            // ── Crisis Response ─────────────────────────────────────
                            if (data.crisis) {
                                hideTyping();
                                showCrisisOverlay(data.crisis);
                                return;
                            }

                            // ── Metadata (Mood/Wellness) ────────────────────────────
                            if (data.fused_mood) {
                                hideTyping();
                                if (data.fused_mood !== 'neutral') {
                                    updateMoodBadge(data.fused_mood, data.confidence, 'fused');
                                }

                                botMessageDiv = appendMessage("", 'bot');
                                botContentEl = botMessageDiv.querySelector('.message-content');

                                if (data.wellness) {
                                    botContentEl.dataset.wellness = JSON.stringify(data.wellness);
                                }
                            }

                            // ── Content Chunk ───────────────────────────────────────
                            if (data.chunk) {
                                fullText += data.chunk;
                                if (botContentEl) {
                                    botContentEl.innerHTML = fullText.replace(/\n/g, '<br>');
                                }
                                scrollToBottom();
                            }
                        } catch (e) {
                            // Skip partial JSON chunks
                        }
                    }
                }
            }

            // Append wellness panel at the end if it exists
            if (botContentEl && botContentEl.dataset.wellness) {
                const wellness = JSON.parse(botContentEl.dataset.wellness);
                botContentEl.innerHTML += buildWellnessPanel(wellness);
                scrollToBottom();
            }

            // Speak the response if TTS is enabled
            if (fullText) {
                speakText(fullText);
            }

        } catch (error) {
            hideTyping();
            appendMessage('I apologize, but I am having trouble connecting to the server. Please make sure the backend is running.', 'bot');
            console.error('Error:', error);
        }
    }

    // ── Crisis Overlay ────────────────────────────────────────────────────────
    function showCrisisOverlay(crisis) {
        crisisMessage.textContent = crisis.message;
        crisisResources.innerHTML = crisis.resources.map(r => `
            <div class="crisis-resource-item">
                <div class="crisis-resource-name">${r.name}</div>
                <div class="crisis-resource-number">${r.number}</div>
            </div>
        `).join('');
        crisisReminder.textContent = crisis.reminder;
        crisisOverlay.style.display = 'flex';
    }

    closeCrisisBtn.addEventListener('click', () => {
        crisisOverlay.style.display = 'none';
        appendMessage('💙 I\'m glad you\'re still here. Whenever you\'re ready, I\'m here to listen.', 'bot');
    });

    // ── Camera Functions ──────────────────────────────────────────────────────
    async function startCamera() {
        try {
            cameraStream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } }
            });
            cameraFeed.srcObject = cameraStream;
            cameraFeed.style.display = 'block';
            capturedImage.style.display = 'none';
            cameraModal.classList.add('active');

            captureBtn.style.display = 'block';
            captureBtn.disabled = false;
            postCaptureControls.style.display = 'none';

            updateStatus('Ready', 'rgba(34, 197, 94, 0.2)', '#4ade80');
            cameraGuide.textContent = 'Position your face in the center and ensure good lighting.';
            moodResult.style.display = 'none';
        } catch (err) {
            alert('Unable to access camera. Please grant camera permissions.');
        }
    }

    function updateStatus(text, bg, color) {
        if (!detectionStatus) return;
        detectionStatus.textContent = text;
        detectionStatus.style.background = bg;
        detectionStatus.style.color = color;
        detectionStatus.style.borderColor = color.replace('1)', '0.3)');
    }

    function stopCamera() {
        if (cameraStream) { cameraStream.getTracks().forEach(t => t.stop()); cameraStream = null; }
        cameraFeed.srcObject = null;
        cameraModal.classList.remove('active');
        moodResult.style.display = 'none';
    }

    function captureFace() {
        if (!cameraStream) return;

        // Flash Effect
        cameraFlash.classList.remove('flash-active');
        void cameraFlash.offsetWidth; // Trigger reflow
        cameraFlash.classList.add('flash-active');

        const ctx = snapshotCanvas.getContext('2d');
        snapshotCanvas.width = cameraFeed.videoWidth;
        snapshotCanvas.height = cameraFeed.videoHeight;
        ctx.drawImage(cameraFeed, 0, 0);

        const imageData = snapshotCanvas.toDataURL('image/jpeg', 0.8);
        capturedImage.src = imageData;

        // UI Swap
        cameraFeed.style.display = 'none';
        capturedImage.style.display = 'block';
        captureBtn.style.display = 'none';
        postCaptureControls.style.display = 'flex';

        updateStatus('Review', 'rgba(139, 92, 246, 0.2)', '#a78bfa');
        cameraGuide.textContent = 'Looking good? Click analyze to detect your mood.';
    }

    function retakeSnapshot() {
        cameraFeed.style.display = 'block';
        capturedImage.style.display = 'none';
        captureBtn.style.display = 'block';
        postCaptureControls.style.display = 'none';
        moodResult.style.display = 'none';

        updateStatus('Ready', 'rgba(34, 197, 94, 0.2)', '#4ade80');
        cameraGuide.textContent = 'Position your face and try again.';
    }

    async function analyzeSnapshot() {
        const imageData = capturedImage.src;
        if (!imageData) return;

        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        updateStatus('Analyzing', 'rgba(234, 179, 8, 0.2)', '#fde047');

        try {
            const resp = await fetch('/api/detect-mood', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData })
            });

            if (!resp.ok) {
                const errorData = await resp.json().catch(() => ({}));
                throw new Error(errorData.message || `Server error (${resp.status})`);
            }

            const result = await resp.json();

            if (result.success) {
                updateStatus('Success', 'rgba(34, 197, 94, 0.2)', '#4ade80');
                displayMoodResult(result);
                detectedImageMood = result.emotion;
                updateMoodBadge(result.emotion, result.confidence, 'image');
            } else {
                updateStatus('Failed', 'rgba(239, 68, 68, 0.2)', '#f87171');
                moodResult.innerHTML = `<h4>⚠️ Detection Failed</h4><p>${result.message || 'Unable to detect mood.'}</p>`;
                moodResult.style.display = 'block';
            }
        } catch (err) {
            console.error('Image analysis error:', err);
            updateStatus('Error', 'rgba(239, 68, 68, 0.2)', '#f87171');
            moodResult.innerHTML = `<h4>❌ Error</h4><p>${err.message || 'Failed to analyze image.'}</p>`;
            moodResult.style.display = 'block';
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fa-solid fa-magic-wand-sparkles"></i> Analyze Mood';
        }
    }

    // ── Voice Controller (Dictation & TTS) ──────────────────────────────────
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isDictating = false;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;

        recognition.onstart = function () {
            isDictating = true;
            dictateBtn.classList.add('recording');
            userInput.placeholder = "Listening...";
        };

        recognition.onresult = function (event) {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            if (finalTranscript) {
                userInput.value = (userInput.value + ' ' + finalTranscript).trim();
            }
        };

        recognition.onerror = function (event) {
            console.error("Speech recognition error", event.error);
            if (event.error === 'not-allowed') {
                appendMessage('🚫 Microphone access denied. Please allow microphone permissions in your browser settings to use dictation.', 'bot');
            } else {
                appendMessage(`⚠️ Voice Error: ${event.error}. Please try again.`, 'bot');
            }
            stopDictation();
        };

        recognition.onend = function () {
            stopDictation();
        };
    } else {
        if (dictateBtn) {
            dictateBtn.addEventListener('click', () => {
                appendMessage('⚠️ Dictation is not supported in this browser. Please try using Chrome or Edge.', 'bot');
            });
        }
        console.warn("Speech Recognition API not supported in this browser.");
    }

    function toggleDictation() {
        if (!recognition) return;
        if (isDictating) {
            recognition.stop();
        } else {
            recognition.lang = getLangCode(langSelect ? langSelect.value : 'English');
            recognition.start();
        }
    }

    function stopDictation() {
        isDictating = false;
        if (dictateBtn) dictateBtn.classList.remove('recording');
        userInput.placeholder = "Type your message here...";
    }

    function getLangCode(langName) {
        const map = {
            'English': 'en-US',
            'Tamil': 'ta-IN',
            'Telugu': 'te-IN',
            'Kannada': 'kn-IN',
            'Malayalam': 'ml-IN'
        };
        return map[langName] || 'en-US';
    }

    if (dictateBtn) {
        dictateBtn.addEventListener('click', toggleDictation);
    }

    // Text to Speech
    if (ttsToggleBtn) {
        ttsToggleBtn.addEventListener('click', () => {
            isTtsEnabled = !isTtsEnabled;
            if (isTtsEnabled) {
                ttsToggleBtn.classList.add('active');
                ttsIcon.className = "fa-solid fa-volume-high";
                ttsText.textContent = "Voice On";
                speakText("Voice output enabled.");
            } else {
                ttsToggleBtn.classList.remove('active');
                ttsIcon.className = "fa-solid fa-volume-xmark";
                ttsText.textContent = "Voice Off";
                if (window.speechSynthesis) window.speechSynthesis.cancel();
            }
        });
    }

    function speakText(text) {
        if (!isTtsEnabled || !window.speechSynthesis) return;

        window.speechSynthesis.cancel();

        // Clean markdown and emojis for speech
        const cleanText = text.replace(/[*_#`~>]/g, '')
            .replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g, '')
            .trim();

        if (!cleanText) return;

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = getLangCode(langSelect ? langSelect.value : 'English');
        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        window.speechSynthesis.speak(utterance);
    }

    // ── Voice Recording (Emotion Analysis) ───────────────────────────────────
    async function startVoiceRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioChunks = [];
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = e => { if (e.data.size > 0) audioChunks.push(e.data); };
            mediaRecorder.onstop = async () => {
                stream.getTracks().forEach(t => t.stop());
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                voiceOverlay.style.display = 'none';

                // Convert WebM to WAV because backend may lack ffmpeg
                try {
                    const wavBlob = await convertWebmToWav(audioBlob);
                    await analyzeVoice(wavBlob);
                } catch (err) {
                    console.error('Audio conversion failed:', err);
                    await analyzeVoice(audioBlob); // Fallback to original
                }
            };
            mediaRecorder.start();
            voiceOverlay.style.display = 'flex';
        } catch (err) {
            alert('Unable to access microphone. Please grant microphone permissions.');
        }
    }

    async function convertWebmToWav(webmBlob) {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const arrayBuffer = await webmBlob.arrayBuffer();
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

        // Simple WAV encoding
        const numChannels = audioBuffer.numberOfChannels;
        const sampleRate = audioBuffer.sampleRate;
        const format = 1; // PCM
        const bitDepth = 16;
        const bytesPerSample = bitDepth / 8;
        const blockAlign = numChannels * bytesPerSample;

        const buffer = audioBuffer.getChannelData(0); // Use mono for smaller size
        const dataLength = buffer.length * bytesPerSample;
        const headerLength = 44;
        const fullBuffer = new ArrayBuffer(headerLength + dataLength);
        const view = new DataView(fullBuffer);

        const writeString = (v, offset, str) => {
            for (let i = 0; i < str.length; i++) v.setUint8(offset + i, str.charCodeAt(i));
        };

        writeString(view, 0, 'RIFF');
        view.setUint32(4, 36 + dataLength, true);
        writeString(view, 8, 'WAVE');
        writeString(view, 12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, format, true);
        view.setUint16(22, 1, true); // Mono
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2, true);
        view.setUint16(34, bitDepth, true);
        writeString(view, 36, 'data');
        view.setUint32(40, dataLength, true);

        let offset = 44;
        for (let i = 0; i < buffer.length; i++, offset += 2) {
            const s = Math.max(-1, Math.min(1, buffer[i]));
            view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
        }

        return new Blob([fullBuffer], { type: 'audio/wav' });
    }

    // ── Song Grid Renderer Helper ─────────────────────────────────────────────
    function renderSongsGrid(songs, limit = null) {
        if (!songs || songs.length === 0) return '';

        const displaySongs = limit ? songs.slice(0, limit) : songs;

        const cardsHtml = displaySongs.map(song => `
            <div class="song-card" 
                 data-url="${song.url}" 
                 data-name="${(song.Name || '').replace(/"/g, '&quot;')}" 
                 data-artist="${(song.Artist || '').replace(/"/g, '&quot;')}"
                 title="Play ${song.Name}">
                <div class="song-play-overlay">
                    <i class="fa-solid fa-play"></i>
                </div>
                <div class="song-info">
                    <span class="song-name">${song.Name}</span>
                    <span class="song-artist">${song.Artist}</span>
                </div>
            </div>`).join('');

        return `<div class="songs-grid">${cardsHtml}</div>`;
    }

    function stopVoiceRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
    }

    async function analyzeVoice(audioBlob) {
        const loadingMsg = appendMessage('<i class="fa-solid fa-spinner fa-spin"></i> Analyzing your voice tone...', 'bot');
        try {
            const fd = new FormData();
            const filename = audioBlob.type === 'audio/wav' ? 'recording.wav' : 'recording.webm';
            fd.append('audio', audioBlob, filename);
            const resp = await fetch('/api/voice-mood', { method: 'POST', body: fd });
            const result = await resp.json();

            loadingMsg.remove();

            if (result.success) {
                detectedVoiceMood = result.emotion;
                updateMoodBadge(result.emotion, result.confidence, 'voice');

                const f = result.features || {};
                const featureText = f.tempo
                    ? `Pitch: ${f.avg_pitch} Hz · Tempo: ${f.tempo} BPM · Energy: ${f.energy}`
                    : '';

                const sugHtml = (result.suggestions || []).map(s => `<li>${s}</li>`).join('');
                const songs = result.songs || [];
                const songsHtml = renderSongsGrid(songs, 6); // Limit to 6 in chat bubble

                let wellnessHtml = buildWellnessPanel(result.wellness);

                appendMessage(`
                    <div class="mood-header">
                        <h3>🎤 Voice Analysis</h3>
                        <span class="emotion-tag emotion-${result.emotion}">${result.emotion.toUpperCase()}</span>
                    </div>
                    <p style="color:#94a3b8;font-size:0.8rem;margin-bottom:10px;">${featureText}</p>
                    <h4>💡 Suggestions:</h4>
                    <ul class="suggestions-list">${sugHtml}</ul>
                    ${songs.length > 0 ? '<h4>🎵 Songs:</h4>' + songsHtml : ''}
                    ${wellnessHtml}
                    <p style="margin-top:12px;color:#94a3b8;font-size:0.8rem;">Your voice emotion is now included in my responses.</p>
                `, 'bot');
            } else {
                appendMessage(`⚠️ Voice analysis failed: ${result.error || 'Unknown error'}. Try speaking for a few seconds.`, 'bot');
            }
        } catch (err) {
            loadingMsg.remove();
            appendMessage('Failed to analyze voice. Please try again.', 'bot');
        }
    }

    // ── Mood Display  ─────────────────────────────────────────────────────────
    function displayMoodResult(result) {
        const sugHtml = (result.suggestions || []).map(s => `<li>${s}</li>`).join('');
        const songs = result.songs || [];
        const songsHtml = renderSongsGrid(songs); // Full results (no limit)
        const wellnessHtml = buildWellnessPanel(result.wellness);

        moodResult.innerHTML = `
            <div class="mood-header">
                <h3>✨ Mood Detected</h3>
                <span class="emotion-tag emotion-${result.emotion}">${result.emotion.toUpperCase()}</span>
            </div>
            <p style="color:#94a3b8;font-size:0.8rem;margin-bottom:15px;">Confidence: ${result.confidence}%</p>
            <h4>💡 Suggestions:</h4>
            <ul class="suggestions-list">${sugHtml}</ul>
            ${songs.length > 0 ? '<h4>🎵 Recommended Songs:</h4>' + songsHtml : ''}
            ${wellnessHtml}
            <button id="done-analysis" class="analyze-btn-premium" style="margin-top:20px; width: 100%;">
                <i class="fa-solid fa-check-circle"></i> Back to Chat
            </button>
        `;
        moodResult.style.display = 'block';


        // Add event listener to the newly created button
        document.getElementById('done-analysis').addEventListener('click', () => {
            stopCamera();
            scrollToBottom();
        });
    }

    function updateMoodBadge(emotion, confidence, source) {
        const icon = source === 'voice' ? '🎤' : source === 'fused' ? '🔮' : '📷';
        // Fix: correctly handle confidence as a decimal (0.0 - 1.0) and display as percentage
        const displayConf = Math.round(confidence <= 1 ? confidence * 100 : confidence);
        const confText = confidence ? ` (${displayConf}%)` : '';
        moodText.innerHTML = `${icon} <span class="emotion-tag emotion-${emotion}">${emotion.toUpperCase()}</span>${confText}`;
        moodBadge.style.display = 'flex';
        updateAvatar(emotion);
    }

    function updateAvatar(emotion) {
        const mouth = document.getElementById('avatar-mouth');
        const eyes = document.querySelectorAll('.eye');

        // Default (Neutral/Happy-ish)
        let mouthPath = "M 35 65 Q 50 75 65 65"; // Smile
        let eyeScaleY = "1";

        if (emotion === 'sad' || emotion === 'fear') {
            mouthPath = "M 35 75 Q 50 65 65 75"; // Frown
        } else if (emotion === 'angry' || emotion === 'stress') {
            mouthPath = "M 35 70 L 65 70"; // Flat/Tense line
        } else if (emotion === 'happy' || emotion === 'surprise') {
            mouthPath = "M 30 65 Q 50 85 70 65"; // Big smile
        }

        if (mouth) mouth.setAttribute('d', mouthPath);
    }

    function clearMood() {
        detectedImageMood = null;
        detectedVoiceMood = null;
        moodBadge.style.display = 'none';
    }


    // ── Mindfulness Timer Logic ───────────────────────────────────────────────
    let timerInterval = null;
    let breathingInterval = null;

    if (timerBtn) timerBtn.onclick = openTimer;
    if (closeTimerBtn) closeTimerBtn.onclick = closeTimer;
    if (startTimerBtn) startTimerBtn.onclick = startTimer;

    function openTimer() { if (timerModal) timerModal.classList.add('active'); }
    function closeTimer() {
        if (timerModal) {
            timerModal.classList.remove('active');
            clearInterval(timerInterval);
            clearInterval(breathingInterval);
            resetTimerUI();
        }
    }

    function resetTimerUI() {
        if (breathingCircle) breathingCircle.className = 'breathing-circle';
        if (breathingText) breathingText.textContent = 'Inhale...';
        if (countdownTimer) countdownTimer.textContent = '02:00';
        if (startTimerBtn) {
            startTimerBtn.disabled = false;
            startTimerBtn.textContent = 'Start Session';
        }
    }

    function startTimer() {
        if (!startTimerBtn) return;
        startTimerBtn.disabled = true;
        startTimerBtn.textContent = 'Progress...';

        let timeLeft = 120;
        timerInterval = setInterval(() => {
            timeLeft--;
            const mins = Math.floor(timeLeft / 60);
            const secs = timeLeft % 60;
            if (countdownTimer) countdownTimer.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                clearInterval(breathingInterval);
                if (breathingText) breathingText.textContent = 'Complete! 🌸';
                setTimeout(closeTimer, 2000);
            }
        }, 1000);

        breathingInterval = setInterval(() => {
            if (!breathingCircle || !breathingText) return;
            breathingCircle.className = 'breathing-circle inhale';
            breathingText.textContent = 'Inhale...';
            setTimeout(() => {
                breathingCircle.className = 'breathing-circle hold';
                breathingText.textContent = 'Hold...';
            }, 4000);
            setTimeout(() => {
                breathingCircle.className = 'breathing-circle exhale';
                breathingText.textContent = 'Exhale...';
            }, 11000);
        }, 19000);
    }

    // ── Profile Logic ─────────────────────────────────────────────────────────
    if (profileForm) {
        profileForm.onsubmit = async (e) => {
            e.preventDefault();
            const bio = profileBio ? profileBio.value : '';
            const history = document.getElementById('profile-history') ? document.getElementById('profile-history').value : '';
            const emName = document.getElementById('profile-em-name') ? document.getElementById('profile-em-name').value : '';
            const emPhone = document.getElementById('profile-em-phone') ? document.getElementById('profile-em-phone').value : '';
            const age = document.getElementById('profile-age') ? document.getElementById('profile-age').value : '';
            const gender = document.getElementById('profile-gender') ? document.getElementById('profile-gender').value : '';
            const fullName = document.getElementById('profile-name') ? document.getElementById('profile-name').value : '';

            try {
                const response = await fetch('/api/profile/update', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        full_name: fullName,
                        age: age,
                        gender: gender,
                        occupation: bio,
                        mental_health_history: history,
                        emergency_contact_name: emName,
                        emergency_contact_phone: emPhone,
                        phone_number: document.getElementById('profile-phone') ? document.getElementById('profile-phone').value : '',
                        email_notifications: document.getElementById('notify-email') ? document.getElementById('notify-email').checked : false,
                        sms_notifications: document.getElementById('notify-sms') ? document.getElementById('notify-sms').checked : false,
                        app_notifications: document.getElementById('notify-app') ? document.getElementById('notify-app').checked : false
                    })
                });
                const data = await response.json();
                if (data.success) {
                    appendMessage("✅ Profile and medical info updated successfully!", "bot");
                    // Update header if name changed
                    if (profileName && document.querySelector('.user-info div:first-child')) {
                        document.querySelector('.user-info div:first-child').textContent = profileName.value;
                    }
                }
            } catch (err) {
                console.error("Profile update error:", err);
            }
        };
    }

    // Close on outside click
    window.onclick = (e) => {
        const cameraModal = document.getElementById('camera-modal');
        const timerModal = document.getElementById('timer-modal');
        const musicModal = document.getElementById('music-modal');
        if (e.target === cameraModal && typeof stopCamera === 'function') stopCamera();
        if (e.target === timerModal) closeTimer();
        if (musicModal && e.target === musicModal) musicModal.classList.remove('active');
    };

    scrollToBottom();

    async function loadSpecialists() {
        if (!doctorListSimple) return;
        try {
            doctorListSimple.innerHTML = '<p style="color:#94a3b8; text-align:center; padding:20px;">⌛ Loading specialists...</p>';
            const resp = await fetch('/api/doctors/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ q: '' })
            });
            const data = await resp.json();

            doctorListSimple.innerHTML = '';
            if (!data.doctors || data.doctors.length === 0) {
                doctorListSimple.innerHTML = '<p style="color:#94a3b8; text-align:center; padding:20px;">No specialists available at the moment.</p>';
                return;
            }
            data.doctors.forEach(dr => {
                const card = document.createElement('div');
                card.className = 'doctor-card-simple';
                card.style = `
                    background: rgba(30, 41, 59, 0.5);
                    border: 1px solid rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 16px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    transition: 0.3s;
                    margin-bottom: 10px;
                `;
                card.innerHTML = `
                    <div>
                        <h4 style="margin:0; color:#fff;">${dr.name}</h4>
                        <p style="margin:5px 0 0; color:#94a3b8; font-size:0.85rem;">${dr.specialization} • ${dr.experience} Exp</p>
                        <div style="margin-top:8px; font-size:0.8rem; color:var(--accent-color);">₹${dr.fees} per session</div>
                        <div style="margin-top:4px; font-size:0.75rem; color:#64748b;"><i class="fa-solid fa-calendar-check"></i> ${dr.availability}</div>
                    </div>
                    <button class="capture-btn" style="width:auto; padding:8px 20px; font-size:0.85rem;" onclick="openBooking('${dr.name}', ${dr.id}, '${dr.availability}')">Book Now</button>
                `;
                doctorListSimple.appendChild(card);
            });
        } catch (err) {
            console.error("Failed to load specialists:", err);
            doctorListSimple.innerHTML = '<p style="color:#ef4444; text-align:center; padding:20px;">Error loading specialists. Please try again.</p>';
        }
    }

    window.openBooking = (name, id, availability) => {
        selectedDoctor = { name, id, availability };
        bookingDrName.innerHTML = `<span style="display:block;">Consulting with ${name}</span>
                                 <span style="font-size:0.8rem; color:#64748b; font-weight:normal;">Availability: ${availability}</span>`;
        bookingStep1.style.display = 'block';
        bookingStep2.style.display = 'none';
        bookingStep3.style.display = 'none';
        bookingModalSimple.style.display = 'flex';
    };

    if (closeBookingSimple) {
        closeBookingSimple.onclick = () => bookingModalSimple.style.display = 'none';
    }

    if (nextToPayment) {
        nextToPayment.onclick = () => {
            if (!bookDate.value || !bookTime.value) {
                alert("Please select a date and time.");
                return;
            }

            // Basic availability validation (Weekend check)
            const dateObj = new Date(bookDate.value);
            const day = dateObj.getDay(); // 0 is Sunday, 6 is Saturday
            const availLower = selectedDoctor.availability.toLowerCase();

            if (availLower.includes("mon-fri") && (day === 0 || day === 6)) {
                alert(`This doctor is only available Mon-Fri. Please pick a weekday.`);
                return;
            }
            if (availLower.includes("mon-sat") && day === 0) {
                alert(`This doctor is not available on Sundays.`);
                return;
            }

            bookingStep1.style.display = 'none';
            bookingStep2.style.display = 'block';
        };
    }

    if (confirmPaymentSim) {
        confirmPaymentSim.onclick = async () => {
            // Simulated backend call
            try {
                const resp = await fetch('/api/appointments/book', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        doctor_id: selectedDoctor.id,
                        date: bookDate.value,
                        time: bookTime.value,
                        type: bookType.value
                    })
                });
                const data = await resp.json();
                if (data.success) {
                    bookingStep2.style.display = 'none';
                    bookingStep3.style.display = 'block';
                }
            } catch (err) {
                alert("Booking failed. Please try again.");
            }
        };
    }

    if (confirmWhatsapp) {
        confirmWhatsapp.onclick = () => {
            const phone = "919000000000"; // Placeholder doctor WhatsApp
            const msg = `Hi ${selectedDoctor.name}, I've booked a ${bookType.value} session for ${bookDate.value} at ${bookTime.value}. I've completed the payment. Please confirm my slot.`;
            window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, '_blank');
            bookingModalSimple.style.display = 'none';
        };
    }

    // ── Consultation Logic ───────────────────────────────────────────────────

    async function loadConsultations() {
        if (!consultationList) return;
        consultationList.innerHTML = '<p style="color:#94a3b8; text-align:center; padding:20px;">⌛ Loading your sessions...</p>';

        try {
            // In a real app, we'd fetch from /api/consultations/active
            // For now, we'll fetch recently booked appointments
            const resp = await fetch('/api/doctors/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ q: '' })
            });
            const data = await resp.json();

            consultationList.innerHTML = '';
            if (!data.doctors || data.doctors.length === 0) {
                consultationList.innerHTML = '<div class="vibrant-card" style="padding:20px; text-align:center; color:#94a3b8;"><i class="fa-solid fa-calendar-day" style="font-size:2rem; margin-bottom:10px; display:block;"></i>No active sessions found.</div>';
                return;
            }

            // Show first 3 doctors as "Active Sessions" for demo purposes
            data.doctors.slice(0, 3).forEach(dr => {
                const card = document.createElement('div');
                card.className = 'doctor-card-simple';
                card.style = `
                    background: rgba(30, 41, 59, 0.5);
                    border: 1px solid rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 16px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    transition: 0.3s;
                    margin-bottom: 10px;
                `;
                card.innerHTML = `
                    <div>
                        <h4 style="margin:0; color:#fff;">Session with ${dr.name}</h4>
                        <p style="margin:5px 0 0; color:#4ade80; font-size:0.85rem;">Status: Ready to Join</p>
                        <div style="margin-top:8px; font-size:0.8rem; color:#94a3b8;">📅 Today • 10:30 AM</div>
                    </div>
                    <div style="display:flex; gap:10px;">
                        <button class="capture-btn" style="width:40px; height:40px; padding:0; border-radius:50%;" onclick="openConsultation('Chat', '${dr.name}')" title="Chat"><i class="fa-solid fa-comment"></i></button>
                        <button class="capture-btn" style="width:40px; height:40px; padding:0; border-radius:50%; background:var(--accent-gradient);" onclick="openConsultation('Video', '${dr.name}')" title="Video Call"><i class="fa-solid fa-video"></i></button>
                    </div>
                `;
                consultationList.appendChild(card);
            });
        } catch (err) {
            console.error("Failed to load consultations:", err);
        }
    }

    window.openConsultation = (type, drName) => {
        try {
            console.log("Opening consultation:", type, drName);

            if (!consultationModal) {
                console.error("consultationModal element is missing!");
                alert("Error: Consultation modal not found.");
                return;
            }
            if (!chatDrName) {
                console.warn("chatDrName element is missing, skipping text update.");
            } else {
                chatDrName.textContent = `Consultation with ${drName}`;
            }

            consultationModal.style.display = 'flex';

            // Reset UI
            if (consultationMedia) {
                consultationMedia.style.display = (type === 'Video' || type === 'Voice') ? 'block' : 'none';
            }
            if (consultationStatus) {
                consultationStatus.textContent = "CONNECTING...";
            }
            if (consultationMessages) {
                consultationMessages.innerHTML = `
                    <div class="message bot-message" style="align-self:center;">
                        <div class="message-content" style="background:rgba(30,41,59,0.8); border:1px solid rgba(255,255,255,0.05); border-radius:12px; font-size:0.85rem; color:#94a3b8;">
                            ${type} Consultation started with ${drName}.
                        </div>
                    </div>
                `;
            }

            if (type === 'Video') {
                // Simulate Video Connection
                setTimeout(() => {
                    if (consultationStatus) consultationStatus.textContent = "LIVE";
                    // Start local camera for simulation
                    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                        .then(stream => {
                            if (consultationVideoLocal) consultationVideoLocal.srcObject = stream;
                            // Remote is just a placeholder/local loop for demo
                            if (consultationVideoRemote) consultationVideoRemote.srcObject = stream;
                            console.log("Camera started successfully for", type);
                        })
                        .catch(err => {
                            console.warn("Camera access denied for consultation", err);
                            alert("Camera/Mic access denied. Please allow permissions in your browser.");
                        });
                }, 2000);
            }
        } catch (e) {
            console.error("Critical error in openConsultation:", e);
            alert("An error occurred while opening the consultation.");
        }
    };


    if (closeConsultation) {
        closeConsultation.onclick = () => {
            consultationModal.style.display = 'none';
            if (consultationVideoLocal.srcObject) {
                consultationVideoLocal.srcObject.getTracks().forEach(track => track.stop());
            }
        };
    }

    if (endCallBtn) {
        endCallBtn.onclick = () => {
            consultationMedia.style.display = 'none';
            if (consultationVideoLocal.srcObject) {
                consultationVideoLocal.srcObject.getTracks().forEach(track => track.stop());
            }
            addConsultationMessage("System", "Call ended by user.");
        };
    }

    document.addEventListener('click', (e) => {
        const target = e.target.closest('#toggle-mic-btn') || e.target.closest('#toggle-video-btn');
        if (!target) return;

        const stream = consultationVideoLocal.srcObject;
        if (!stream) return;

        if (target.id === 'toggle-mic-btn') {
            const audioTracks = stream.getAudioTracks();
            if (audioTracks.length > 0) {
                const isEnabled = audioTracks[0].enabled;
                audioTracks[0].enabled = !isEnabled;
                target.style.color = isEnabled ? '#ef4444' : '#fff';
                target.innerHTML = isEnabled ? '<i class="fa-solid fa-microphone-slash"></i>' : '<i class="fa-solid fa-microphone"></i>';
            }
        } else if (target.id === 'toggle-video-btn') {
            const videoTracks = stream.getVideoTracks();
            if (videoTracks.length > 0) {
                const isEnabled = videoTracks[0].enabled;
                videoTracks[0].enabled = !isEnabled;
                target.style.color = isEnabled ? '#ef4444' : '#fff';
                target.innerHTML = isEnabled ? '<i class="fa-solid fa-video-slash"></i>' : '<i class="fa-solid fa-video"></i>';
            }
        }
    });


    if (sendConsultationBtn) {
        sendConsultationBtn.onclick = () => {
            const msg = consultationInput.value.trim();
            if (!msg) return;
            addConsultationMessage("You", msg);
            consultationInput.value = '';

            // Auto response from "Doctor"
            setTimeout(() => {
                addConsultationMessage("Doctor", "Thank you for sharing. I'm reviewing your recent mood history now.");
            }, 1500);
        };
    }

    function addConsultationMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = sender === 'You' ? 'message user-message' : 'message bot-message';
        msgDiv.innerHTML = `
            <div class="message-content" style="max-width:85%;">
                <p><strong>${sender}:</strong> ${text}</p>
            </div>
        `;
        consultationMessages.appendChild(msgDiv);
        consultationMessages.scrollTop = consultationMessages.scrollHeight;
    }

    // ── Medical History Logic ───────────────────────────────────────────────
    async function loadHistory() {
        const historyList = document.getElementById('history-list');
        if (!historyList) return;

        historyList.innerHTML = '<p style="color:#94a3b8; text-align:center; padding:20px;">⌛ Loading your history...</p>';

        try {
            const resp = await fetch('/api/appointments/patient');
            const data = await resp.json();

            historyList.innerHTML = '';
            if (!data.appointments || data.appointments.length === 0) {
                historyList.innerHTML = '<div class="vibrant-card" style="padding:20px; text-align:center; color:#94a3b8;"><i class="fa-solid fa-file-medical" style="font-size:2rem; margin-bottom:10px; display:block;"></i>No previous consultations found.</div>';
                return;
            }

            data.appointments.forEach(app => {
                const card = document.createElement('div');
                card.className = 'doctor-card-simple';
                card.style = `
                    background: rgba(30, 41, 59, 0.5);
                    border: 1px solid rgba(255,255,255,0.05);
                    padding: 20px;
                    border-radius: 16px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                `;

                const hasReport = app.status === 'Completed' || app.prescription || app.notes;

                card.innerHTML = `
                    <div>
                        <h4 style="margin:0; color:#fff;">Consultation with ${app.doctor_name}</h4>
                        <p style="margin:5px 0 0; color:#94a3b8; font-size:0.85rem;">${app.specialization} • ${app.type}</p>
                        <div style="margin-top:8px; font-size:0.8rem; color:#64748b;">📅 ${app.date} • ${app.time}</div>
                    </div>
                    <div style="display:flex; gap:10px;">
                        ${hasReport ? `
                            <a href="/api/consultations/report/${app.id}" class="capture-btn" style="width:auto; padding:8px 15px; font-size:0.8rem; text-decoration:none; display:flex; align-items:center; gap:5px;" target="_blank">
                                <i class="fa-solid fa-download"></i> PDF Report
                            </a>
                        ` : `
                            <span style="font-size:0.75rem; color:#64748b; font-style:italic;">Report Pending</span>
                        `}
                    </div>
                `;
                historyList.appendChild(card);
            });
        } catch (err) {
            console.error("Failed to load history:", err);
            historyList.innerHTML = '<p style="color:#ef4444; text-align:center; padding:20px;">Error loading history.</p>';
        }
    }

    // ── Notifications Logic ─────────────────────────────────────────────────
    function showNotification(title, message, icon = 'fa-bell') {
        const container = document.getElementById('notification-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.style = `
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid var(--accent-color);
            border-radius: 12px;
            padding: 15px 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            gap: 15px;
            min-width: 300px;
            max-width: 400px;
            pointer-events: auto;
            animation: slideInRight 0.5s ease-out forwards;
            position: relative;
            overflow: hidden;
        `;

        toast.innerHTML = `
            <div style="width:40px; height:40px; background:var(--accent-gradient); border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <i class="fa-solid ${icon}" style="color:#fff;"></i>
            </div>
            <div style="flex:1;">
                <div style="font-weight:600; color:#fff; font-size:0.95rem;">${title}</div>
                <div style="color:#94a3b8; font-size:0.85rem; margin-top:2px;">${message}</div>
            </div>
            <div id="toast-progress" style="position:absolute; bottom:0; left:0; height:3px; background:var(--accent-color); width:100%; transition:5s linear;"></div>
        `;

        container.appendChild(toast);

        // Progress bar animation
        setTimeout(() => {
            const progress = toast.querySelector('#toast-progress');
            if (progress) progress.style.width = '0%';
        }, 10);

        // Remove after 5s
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.5s ease-out forwards';
            setTimeout(() => toast.remove(), 500);
        }, 5000);
    }

    async function checkNotifications() {
        try {
            const resp = await fetch('/api/notifications/pending');
            const data = await resp.json();

            if (data.success && data.notifications.length > 0) {
                data.notifications.forEach(notif => {
                    const title = notif.type === 'reminder_1h' ? 'Upcoming Session' : 'Appointment Reminder';
                    const msg = `Your session with ${notif.doctor_name} is in ${notif.type === 'reminder_1h' ? '1 hour' : '1 day'} (${notif.date} at ${notif.time}).`;
                    showNotification(title, msg, 'fa-calendar-check');
                });
            }
        } catch (err) {
            console.warn("Notification check failed:", err);
        }
    }

    // Check for notifications every 1 minute
    setInterval(checkNotifications, 60000);
    // Initial check
    setTimeout(checkNotifications, 3000);

    // ── Map Integration ──────────────────────────────────────────────────
    let map;
    let markers = [];
    let userMarker;
    let mapInitialized = false;

    // Google Maps API script callback
    window.initMapPlaceholder = function () {
        console.log("Google Maps API script loaded.");
        if (document.querySelector('[data-tab="maps"]').classList.contains('active')) {
            initMap();
        }
    };

    async function initMap() {
        if (mapInitialized) return;
        const mapElement = document.getElementById('map');
        if (!mapElement) return;

        // Default: Chennai (can be updated to a global default)
        const defaultPos = { lat: 13.0827, lng: 80.2707 };

        try {
            map = new google.maps.Map(mapElement, {
                zoom: 14,
                center: defaultPos,
                mapId: 'DEMO_MAP_ID', // Use a demo ID or your own
                disableDefaultUI: false,
                mapTypeControl: false,
                streetViewControl: false,
                fullscreenControl: true,
                styles: [
                    { "elementType": "geometry", "stylers": [{ "color": "#121926" }] },
                    { "elementType": "labels.text.stroke", "stylers": [{ "color": "#121926" }] },
                    { "elementType": "labels.text.fill", "stylers": [{ "color": "#8ea3bf" }] },
                    { "featureType": "water", "elementType": "geometry", "stylers": [{ "color": "#17263c" }] }
                ]
            });

            mapInitialized = true;
            getUserLocationAndFetch();

        } catch (e) {
            console.error("Map initialization failed:", e);
            stats.innerHTML = `<i class="fa-solid fa-exclamation-triangle"></i> Map failed. Check API configuration.`;
        }
    }

    function getUserLocationAndFetch() {
        const stats = document.getElementById('map-stats');
        stats.innerHTML = `<i class="fa-solid fa-crosshairs fa-pulse"></i> Getting your precise location...`;

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };

                    console.log("User located at:", pos);
                    map.setCenter(pos);

                    // Clear old user marker
                    if (userMarker) userMarker.setMap(null);

                    userMarker = new google.maps.Marker({
                        position: pos,
                        map: map,
                        title: "You are here",
                        icon: {
                            path: google.maps.SymbolPath.CIRCLE,
                            scale: 8,
                            fillColor: "#3b82f6",
                            fillOpacity: 1,
                            strokeColor: "#ffffff",
                            strokeWeight: 2,
                        }
                    });

                    fetchNearbyFacilities(pos.lat, pos.lng);
                },
                (error) => {
                    console.warn("Geolocation Error:", error.message);
                    let msg = "Location denied. Using default area.";
                    if (error.code === 3) msg = "Location timeout. Try again.";

                    stats.innerHTML = `<i class="fa-solid fa-exclamation-circle"></i> ${msg}`;
                    // Fallback to Chennai or a known default
                    const defaultPos = { lat: 13.0827, lng: 80.2707 };
                    fetchNearbyFacilities(defaultPos.lat, defaultPos.lng);
                },
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );
        } else {
            stats.innerHTML = `<i class="fa-solid fa-exclamation-triangle"></i> Browser doesn't support geolocation.`;
            const defaultPos = { lat: 13.0827, lng: 80.2707 };
            fetchNearbyFacilities(defaultPos.lat, defaultPos.lng);
        }
    }

    let currentFacilities = [];

    async function fetchNearbyFacilities(lat, lng) {
        const stats = document.getElementById('map-stats');
        const posText = `<i class="fa-solid fa-location-dot"></i> ${lat.toFixed(4)}, ${lng.toFixed(4)}`;
        stats.innerHTML = `${posText} | <i class="fa-solid fa-spinner fa-spin"></i> Loading facilities...`;

        try {
            const response = await fetch('/api/hospitals/nearby', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lat, lng, radius: 50 })
            });
            const data = await response.json();

            if (data.success) {
                currentFacilities = data.facilities;
                console.log("Facilities fetched:", currentFacilities.length);
                renderFacilities(currentFacilities);
                stats.innerHTML = `${posText} | <i class="fa-solid fa-check-circle"></i> ${data.facilities.length} medical hubs found.`;
            } else {
                stats.innerHTML = `${posText} | <i class="fa-solid fa-info-circle"></i> No facilities found in this area.`;
            }
        } catch (err) {
            console.error("Fetch error:", err);
            stats.innerHTML = `${posText} | <i class="fa-solid fa-wifi"></i> Connection error.`;
        }
    }

    function renderFacilities(facilities) {
        clearMarkers();
        facilities.forEach(fac => addFacilityMarker(fac));
    }

    function filterFacilities(type) {
        console.log("Filtering map by:", type);
        if (!currentFacilities.length) {
            showNotification("Hold on", "Wait for the map to finish loading your location.", "fa-clock");
            return;
        }

        if (!type || type === 'all') {
            renderFacilities(currentFacilities);
            updateStatsBar(currentFacilities.length, 'total');
            return;
        }

        const filtered = currentFacilities.filter(f => {
            const name = (f.name || '').toLowerCase();
            const desc = (f.description || '').toLowerCase();
            const fType = (f.type || '').toLowerCase();

            if (type === 'mental') {
                return name.includes('mental') || name.includes('wellness') || name.includes('psych') || name.includes('mind') ||
                    desc.includes('mental') || desc.includes('therapy') || desc.includes('counseling') ||
                    fType.includes('clinic') || fType.includes('wellness');
            } else if (type === 'hospital') {
                return name.includes('hospital') || fType.includes('hospital');
            }
            return true;
        });

        renderFacilities(filtered);
        updateStatsBar(filtered.length, type);
    }

    function updateStatsBar(count, type) {
        const stats = document.getElementById('map-stats');
        const posPart = stats.innerHTML.split('|')[0] || '';
        const icon = type === 'mental' ? 'fa-brain' : (type === 'hospital' ? 'fa-hospital' : 'fa-list');
        stats.innerHTML = `${posPart} | <i class="fa-solid ${icon}"></i> Showing ${count} ${type} markers.`;
    }

    function addFacilityMarker(fac) {
        let iconUrl = 'https://cdn-icons-png.flaticon.com/512/4320/4320337.png'; // Hospital
        const name = (fac.name || '').toLowerCase();
        if (name.includes('mental') || name.includes('wellness') || name.includes('psych') || name.includes('mind')) {
            iconUrl = 'https://cdn-icons-png.flaticon.com/512/3062/3062276.png'; // Brain
        }

        const marker = new google.maps.Marker({
            position: { lat: fac.latitude, lng: fac.longitude },
            map: map,
            title: fac.name,
            icon: { url: iconUrl, scaledSize: new google.maps.Size(35, 35) },
            animation: google.maps.Animation.DROP
        });

        const infoWindow = new google.maps.InfoWindow({
            content: `
                <div class="info-window-card">
                    <h4 style="margin:0; color:var(--accent-color);">${fac.name}</h4>
                    <p style="margin:8px 0; font-size:0.85rem;"><i class="fa-solid fa-map-marker-alt"></i> ${fac.location}</p>
                    <p style="margin:10px 0; font-size:0.8rem; line-height:1.4; color:#334155;">${fac.description}</p>
                    <div style="display:flex; gap:10px; margin-top:10px;">
                        <a href="tel:${fac.contact}" class="vibrant-btn" style="background:#10b981; flex:1; text-align:center; padding:8px; border-radius:8px; text-decoration:none; color:white; font-size:0.8rem;"><i class="fa-solid fa-phone"></i> Call</a>
                        <a href="https://www.google.com/maps/dir/?api=1&destination=${fac.latitude},${fac.longitude}" target="_blank" class="vibrant-btn" style="flex:1; text-align:center; padding:8px; border-radius:8px; text-decoration:none; color:white; font-size:0.8rem;"><i class="fa-solid fa-location-arrow"></i> Nav</a>
                    </div>
                </div>
            `
        });

        marker.addListener('click', () => infoWindow.open(map, marker));
        markers.push(marker);
    }

    function clearMarkers() {
        markers.forEach(m => m.setMap(null));
        markers = [];
    }

    // Tabs and Buttons
    const mapTabBtn = document.querySelector('[data-tab="maps"]');
    if (mapTabBtn) {
        mapTabBtn.addEventListener('click', () => {
            setTimeout(() => { if (typeof google !== 'undefined') initMap(); }, 100);
        });
    }

    async function searchLocation() {
        const input = document.getElementById('manual-location-input');
        const address = input.value.trim();
        if (!address) return;

        const stats = document.getElementById('map-stats');
        stats.innerHTML = `<i class="fa-solid fa-search fa-pulse"></i> Searching for "${address}"...`;

        try {
            const resp = await fetch('/api/geocode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ address })
            });
            const data = await resp.json();

            if (data.success) {
                const lat = data.lat;
                const lng = data.lng;
                const pos = { lat, lng };

                console.log("Geocoded:", data.formatted, pos);
                map.setCenter(pos);
                map.setZoom(13);

                if (userMarker) userMarker.setMap(null);
                userMarker = new google.maps.Marker({
                    position: pos,
                    map: map,
                    title: data.formatted || address,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 9,
                        fillColor: "#ef4444",
                        fillOpacity: 1,
                        strokeColor: "#ffffff",
                        strokeWeight: 2,
                    }
                });

                fetchNearbyFacilities(lat, lng);
            } else {
                console.error("Geocode error:", data.error);
                let msg = `Could not find "${address}".`;
                if (data.error === 'ZERO_RESULTS') msg = `No results for "${address}". Try "Vellore, Tamil Nadu".`;
                else if (data.error === 'REQUEST_DENIED') msg = `API key error. Please check the server API key.`;
                stats.innerHTML = `<i class="fa-solid fa-exclamation-triangle"></i> ${msg}`;
            }
        } catch (err) {
            console.error("Search error:", err);
            stats.innerHTML = `<i class="fa-solid fa-wifi"></i> Network error during search.`;
        }
    }

    document.getElementById('search-location-btn')?.addEventListener('click', searchLocation);
    document.getElementById('manual-location-input')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchLocation();
    });

    document.getElementById('find-hospitals-btn')?.addEventListener('click', () => filterFacilities('hospital'));
    document.getElementById('find-mental-btn')?.addEventListener('click', () => filterFacilities('mental'));
    document.getElementById('find-all-btn')?.addEventListener('click', () => filterFacilities('all'));
    document.getElementById('locate-me-btn')?.addEventListener('click', () => {
        document.getElementById('manual-location-input').value = '';
        getUserLocationAndFetch();
    });

    scrollToBottom();
});
