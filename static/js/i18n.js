const i18n = {
    en: {
        chat: "Chat",
        doctors: "Doctors",
        nearby: "Nearby",
        journey: "My Journey",
        challenges: "Challenges",
        journal: "Journal",
        community: "Community",
        profile: "Profile",
        find_specialist: "Find a Specialist",
        nearby_hospitals: "Nearby Hospitals & Clinics",
        emergency_support: "Emergency Support",
        book_appointment: "Book Appointment",
        update_profile: "Update Profile",
        mental_health_history: "Mental Health History",
        emergency_contact: "Emergency Contact",
        emergency_phone: "Emergency Phone",
        history_history_label: "Share your past experiences if any...",
        name_label: "Full Name",
        phone_label: "Phone Number"
    },
    ta: {
        chat: "அரட்டை",
        doctors: "மருத்துவர்கள்",
        nearby: "அருகிலுள்ளவை",
        journey: "எனது பயணம்",
        challenges: "சவால்கள்",
        journal: "நாட்குறிப்பு",
        community: "சமூகம்",
        profile: "சுயவிவரம்",
        find_specialist: "ஒரு நிபுணரைத் தேடுங்கள்",
        nearby_hospitals: "அருகிலுள்ள மருத்துவமனைகள்",
        emergency_support: "அவசர உதவி",
        book_appointment: "முன்பதிவு செய்யுங்கள்",
        update_profile: "சுயவிவரத்தைப் புதுப்பிக்கவும்",
        mental_health_history: "மனநல வரலாறு",
        emergency_contact: "அவசர தொடர்பு",
        emergency_phone: "அவசர தொலைபேசி",
        history_history_label: "உங்கள் கடந்தகால அனுபவங்களைப் பகிரவும்...",
        name_label: "முழு பெயர்",
        phone_label: "தொலைபேசி எண்"
    }
};

window.currentLang = 'en';

function toggleLanguage() {
    window.currentLang = window.currentLang === 'en' ? 'ta' : 'en';
    const langData = i18n[window.currentLang];

    // Update Tabs
    document.querySelector('[data-tab="chat"]').innerHTML = `<i class="fa-solid fa-comment-dots"></i> ${langData.chat}`;
    document.querySelector('[data-tab="doctors"]').innerHTML = `<i class="fa-solid fa-user-doctor"></i> ${langData.doctors}`;
    document.querySelector('[data-tab="nearby"]').innerHTML = `<i class="fa-solid fa-map-location-dot"></i> ${langData.nearby}`;
    document.querySelector('[data-tab="dashboard"]').innerHTML = `<i class="fa-solid fa-chart-line"></i> ${langData.journey}`;
    document.querySelector('[data-tab="challenges"]').innerHTML = `<i class="fa-solid fa-trophy"></i> ${langData.challenges}`;
    document.querySelector('[data-tab="journal"]').innerHTML = `<i class="fa-solid fa-book"></i> ${langData.journal}`;
    document.querySelector('[data-tab="community"]').innerHTML = `<i class="fa-solid fa-users"></i> ${langData.community}`;
    document.querySelector('[data-tab="profile"]').innerHTML = `<i class="fa-solid fa-user"></i> ${langData.profile}`;

    // Update Headers
    const doctorsHeader = document.querySelector('#tab-doctors h2');
    if (doctorsHeader) doctorsHeader.textContent = `🔍 ${langData.find_specialist}`;

    const nearbyHeader = document.querySelector('#tab-nearby h2');
    if (nearbyHeader) nearbyHeader.textContent = `🏥 ${langData.nearby_hospitals}`;

    const emergencyHeader = document.querySelector('.emergency-box h3');
    if (emergencyHeader) emergencyHeader.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${langData.emergency_support}`;

    // Update Profile Tab
    const profileHeader = document.querySelector('#tab-profile h2');
    if (profileHeader) profileHeader.textContent = `👤 ${langData.profile}`;

    const updateBtn = document.querySelector('#profile-form button');
    if (updateBtn) updateBtn.textContent = langData.update_profile;

    // Update labels in profile
    const labels = document.querySelectorAll('#tab-profile label');
    labels.forEach(label => {
        if (label.textContent.includes("Mental Health")) label.textContent = langData.mental_health_history;
        if (label.textContent.includes("Emergency Contact Name")) label.textContent = langData.emergency_contact;
        if (label.textContent.includes("Emergency Contact Phone")) label.textContent = langData.emergency_phone;
    });
}

document.getElementById('lang-toggle').addEventListener('click', toggleLanguage);
