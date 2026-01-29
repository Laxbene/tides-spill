import streamlit as st
import random

# --- STYLING (Custom CSS für Hitster-Look) ---
st.set_page_config(page_title="History Hitster", page_icon="🎸", layout="centered")

st.markdown("""
<style>
    .main {
        background-color: #121212;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
    }
    .hitster-card {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        border: 2px solid #333;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    .event-title {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 10px;
    }
    .year-display {
        font-size: 48px;
        font-weight: 800;
        color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# --- DATEN ---
if 'events' not in st.session_state:
    st.session_state.events = [
        {"event": "Bau der Pyramiden von Gizeh", "year": -2560},
        {"event": "Gründung von Rom", "year": -753},
        {"event": "Untergang von Pompeji", "year": 79},
        {"event": "Krönung Karls des Großen", "year": 800},
        {"event": "Entdeckung Amerikas", "year": 1492},
        {"event": "Französische Revolution", "year": 1789},
        {"event": "Untergang der Titanic", "year": 1912},
        {"event": "Mondlandung (Apollo 11)", "year": 1969},
        {"event": "Mauerfall in Berlin", "year": 1989},
        {"event": "Einführung des iPhones", "year": 2007}
    {"event": "Beginn der ersten Olympischen Spiele", "year": -776},
    {"event": "Ermordung von Julius Cäsar", "year": -44},
    {"event": "Bau der Großen Chinesischen Mauer (Beginn)", "year": -214},
    {"event": "Krönung von Kleopatra zur Königin", "year": -51},
    {"event": "Erfindung des Buchdrucks (Gutenberg)", "year": 1440},
    {"event": "Veröffentlichung von Martin Luthers 95 Thesen", "year": 1517},
    {"event": "Ende des Dreißigjährigen Krieges", "year": 1648},
    {"event": "Unabhängigkeitserklärung der USA", "year": 1776},
    {"event": "Schlacht bei Waterloo (Napoleon)", "year": 1815},
    {"event": "Erfindung des Telefons durch Alexander Graham Bell", "year": 1876},
    {"event": "Erster moderner Marathon", "year": 1896},
    {"event": "Beginn des Ersten Weltkriegs", "year": 1914},
    {"event": "Einführung des Frauenwahlrechts in Deutschland", "year": 1918},
    {"event": "Entdeckung des Penicillins durch Alexander Fleming", "year": 1928},
    {"event": "Ende des Zweiten Weltkriegs", "year": 1945},
    {"event": "Gründung der Vereinten Nationen (UN)", "year": 1945},
    {"event": "Krönung von Queen Elizabeth II.", "year": 1953},
    {"event": "Erscheinen des ersten Beatles-Albums", "year": 1963},
    {"event": "Attentat auf Martin Luther King Jr.", "year": 1968},
    {"event": "Erfindung des World Wide Web (CERN)", "year": 1989},
    {"event": "Wiedervereinigung Deutschlands", "year": 1990},
    {"event": "Auflösung der Sowjetunion", "year": 1991},
    {"event": "Veröffentlichung des ersten Harry Potter Bandes", "year": 1997},
    {"event": "Einführung des Euro als Bargeld", "year": 2002},
    {"event": "Gründung von Facebook", "year": 2004},
    {"event": "Beginn des Arabischen Frühlings", "year": 2010},
    {"event": "Erstes Foto eines Schwarzen Lochs", "year": 2019},
    {"event": "Beginn der COVID-19 Pandemie", "year": 2020},
    {"event": "Krönung von König Charles III.", "year": 2023},
    {"event": "Zerstörung der Bibliothek von Alexandria (Großbrand)", "year": -48}

    ]

def init_game():
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_event' not in st.session_state:
        st.session_state.current_event = random.choice(st.session_state.events)
    if 'phase' not in st.session_state:
        st.session_state.phase = "guess" # guess oder result

def reset_round():
    st.session_state.current_event = random.choice(st.session_state.events)
    st.session_state.phase = "guess"
    st.rerun()

init_game()

# --- HEADER ---
st.title("🎸 History Hitster")
st.write(f"Dein Punktestand: **{st.session_state.score}**")

# --- SPIELFELD ---
event = st.session_state.current_event

# Die "Karte"
st.markdown(f"""
    <div class="hitster-card">
        <div style="font-size: 0.8em; color: #888; text-transform: uppercase; letter-spacing: 2px;">Historisches Ereignis</div>
        <div class="event-title">{event['event']}</div>
    </div>
""", unsafe_allow_html=True)

if st.session_state.phase == "guess":
    # Zeitstrahl Slider
    st.write("### Ordne das Ereignis ein:")
    user_guess = st.slider("", -3000, 2025, 1900, step=1, help="Schiebe den Regler zum richtigen Jahr")
    
    # Feinjustierung für mobiles Tippen / Präzision
    fine_tune = st.number_input("Präzise Jahreszahl eingeben:", value=user_guess)

    if st.button("RAUS MIT DER KARTE!"):
        st.session_state.guess = fine_tune
        st.session_state.phase = "result"
        st.rerun()

else:
    # RESULTAT PHASE
    guess = st.session_state.guess
    correct = event['year']
    diff = abs(guess - correct)
    
    st.markdown(f"""
        <div class="hitster-card" style="border-color: {'#28a745' if diff <= 10 else '#dc3545'}">
            <div style="color: #888;">Das richtige Jahr war:</div>
            <div class="year-display">{correct}</div>
            <div style="color: #888;">Deine Schätzung: {guess}</div>
        </div>
    """, unsafe_allow_html=True)

    if diff == 0:
        st.success("🎯 Wahnsinn! Ein direkter Hit! +20 Punkte")
        points = 20
    elif diff <= 10:
        st.info(f"✨ Sehr nah dran! Nur {diff} Jahre Differenz. +10 Punkte")
        points = 10
    elif diff <= 50:
        st.warning(f"Oha, {diff} Jahre daneben. Aber okay. +2 Punkte")
        points = 2
    else:
        st.error(f"Leider weit daneben ({diff} Jahre). 0 Punkte.")
        points = 0
    
    if st.button("Nächste Karte ziehen ➡️"):
        st.session_state.score += points
        reset_round()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Einstellungen")
    if st.button("Spiel neustarten"):
        st.session_state.score = 0
        reset_round()
    st.markdown("---")
    st.write("Versuche so nah wie möglich an das Jahr heranzukommen. Je näher du bist, desto mehr Punkte gibt es!")
