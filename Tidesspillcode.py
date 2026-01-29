import streamlit as st
import random

# --- DATEN ---
HISTORICAL_EVENTS = [
    {"event": "Ende des 2. Weltkriegs", "year": 1945},
    {"event": "Fall der Berliner Mauer", "year": 1989},
    {"event": "Französische Revolution", "year": 1789},
    {"event": "Mondlandung", "year": 1969},
    {"event": "Entdeckung Amerikas", "year": 1492},
    {"event": "Bau der Chinesischen Mauer", "year": -214},
    {"event": "Untergang der Titanic", "year": 1912},
    {"event": "Bau der Pyramiden von Gizeh (ca.)", "year": -2560},
    {"event": "Erfindung der Keilschrift (ca.)", "year": -3400},
    {"event": "Gründung von Rom (Sage)", "year": -753}
]

def initialize_game():
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_event' not in st.session_state:
        st.session_state.current_event = random.choice(HISTORICAL_EVENTS)
    if 'answered' not in st.session_state:
        st.session_state.answered = False

def next_question():
    st.session_state.current_event = random.choice(HISTORICAL_EVENTS)
    st.session_state.answered = False
    st.rerun()

# --- UI SETUP ---
st.set_page_config(page_title="History Timeline", layout="wide")

initialize_game()

st.title("⏳ Der ultimative Zeitstrahl (-5000 bis heute)")
st.sidebar.metric("Gesamt-Score", st.session_state.score)

event = st.session_state.current_event

# Ereignis-Anzeige
st.markdown(f"### Aktuelles Ereignis:")
st.info(f"## {event['event']}")

# --- DER ZEITSTRAHL ---
st.write("---")
if not st.session_state.answered:
    # Grobe Auswahl über Slider
    slider_val = st.slider("Wähle den ungefähren Zeitpunkt:", -5000, 2025, 0)
    
    # Feinjustierung (Wichtig, da der Slider bei 7000 Jahren Range springt)
    user_guess = st.number_input("Feinjustierung (genaues Jahr):", value=slider_val)
    
    if st.button("Antwort einloggen 🔒", use_container_width=True):
        st.session_state.answered = True
        st.session_state.last_guess = user_guess
        st.rerun()

# --- GRAFISCHE AUSWERTUNG ---
if st.session_state.answered:
    guess = st.session_state.last_guess
    correct = event['year']
    diff = abs(guess - correct)
    
    # Spalten für die visuelle Gegenüberstellung
    col1, col2, col3 = st.columns(3)
    col1.metric("Deine Schätzung", guess)
    col2.metric("Tatsächliches Jahr", correct, delta=int(guess-correct)*-1)
    
    # Grafischer Balken: Wie nah warst du dran? (Logarithmisch gedacht)
    # 0 Differenz = 100% Fortschrittsbalken
    proximity = max(0, 100 - (diff / 10)) # Nur als visuelles Gimmick
    st.write("**Deine Genauigkeit:**")
    st.progress(min(int(proximity), 100))

    # Visueller Zeitstrahl-Vergleich
    # Wir zeigen einen kleinen Ausschnitt der Geschichte als Grafik-Ersatz
    st.write("---")
    
    if diff == 0:
        st.success(f"🎯 Volltreffer! Es war genau {correct}. (+20 Punkte)")
        st.session_state.score += 20
    elif diff <= 50:
        st.warning(f"Sehr nah dran! Nur {diff} Jahre daneben. Es war {correct}. (+5 Punkte)")
        st.session_state.score += 5
    else:
        st.error(f"Leider weit weg. Die Differenz beträgt {diff} Jahre. Es war {correct}.")

    if st.button("Nächstes Ereignis ➡️", use_container_width=True):
        next_question()

# Sidebar Anleitung
with st.sidebar:
    st.markdown("""
    **Legende:**
    * 0 Jahre Diff: 20 Pkt
    * bis 50 Jahre: 5 Pkt
    * darüber: 0 Pkt
    """)
