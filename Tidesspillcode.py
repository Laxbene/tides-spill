import streamlit as st
import random

# --- DATEN ---
HISTORICAL_EVENTS = [
    {"event": "Ende des 2. Weltkriegs", "year": 1945, "range": (1900, 2025)},
    {"event": "Der Fall der Berliner Mauer", "year": 1989, "range": (1900, 2025)},
    {"event": "Die Französische Revolution", "year": 1789, "range": (1700, 1900)},
    {"event": "Landung auf dem Mond", "year": 1969, "range": (1900, 2025)},
    {"event": "Entdeckung Amerikas", "year": 1492, "range": (1000, 1600)},
    {"event": "Beginn der Französischen Revolution", "year": 1789, "range": (1700, 1850)},
    {"event": "Bau der Chinesischen Mauer", "year": -214, "range": (-500, 500)},
    {"event": "Untergang der Titanic", "year": 1912, "range": (1850, 1950)},
    {"event": "Gründung von Rom", "year": -753, "range": (-1000, 0)},
    {"event": "Erfindung des iPhone", "year": 2007, "range": (1990, 2025)}
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

# --- UI ---
st.set_page_config(page_title="History Slider", layout="centered")
initialize_game()

st.title("🎯 History Timeline Slider")
st.write(f"Aktueller Score: **{st.session_state.score}**")

event = st.session_state.current_event

# Card-Design für das Ereignis
st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
    <h2 style="margin: 0;">{event['event']}</h2>
</div>
""", unsafe_allow_html=True)

st.write("") # Abstand

# --- DER ZEITSTRAHL (SLIDER) ---
# Wir nutzen den Range aus den Daten, damit der Slider immer Sinn macht
min_year, max_year = event['range']

if not st.session_state.answered:
    # Der Slider als Zeitlinie
    user_guess = st.slider(
        "Bewege den Regler auf das richtige Jahr:",
        min_value=min_year,
        max_value=max_year,
        value=sum(event['range']) // 2 # Startet in der Mitte des Bereichs
    )
    
    if st.button("Zeitpunkt festlegen 📍", use_container_width=True):
        st.session_state.answered = True
        st.session_state.last_guess = user_guess
        st.rerun()

# --- AUSWERTUNG ---
if st.session_state.answered:
    guess = st.session_state.last_guess
    correct = event['year']
    diff = abs(guess - correct)
    
    # Anzeige der Positionen
    st.info(f"Deine Wahl: **{guess}** | Lösung: **{correct}**")
    
    if diff == 0:
        st.success("🎯 Perfekt! Du bist ein Historiker!")
        st.session_state.score += 10
    elif diff <= 3:
        st.warning(f"Fast! Nur {diff} Jahre daneben.")
        st.session_state.score += 5
    else:
        st.error(f"Leider daneben. Differenz: {diff} Jahre.")

    if st.button("Nächstes Ereignis ➡️", use_container_width=True):
        next_question()
