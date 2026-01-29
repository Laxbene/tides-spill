import streamlit as st
import random

# --- KONFIGURATION & DATEN ---
HISTORICAL_EVENTS = [
    {"event": "Ende des 2. Weltkriegs", "year": 1945},
    {"event": "Der Fall der Berliner Mauer", "year": 1989},
    {"event": "Die Französische Revolution", "year": 1789},
    {"event": "Landung der ersten Menschen auf dem Mond", "year": 1969},
    {"event": "Entdeckung Amerikas durch Kolumbus", "year": 1492},
    {"event": "Beginn des Baues der Chinesischen Mauer (Qin-Dynastie)", "year": -214},
    {"event": "Einführung des Euro als Bargeld", "year": 2002},
    {"event": "Untergang der Titanic", "year": 1912},
    {"event": "Krönung Karls des Großen zum Kaiser", "year": 800},
    {"event": "Erfindung des Buchdrucks (Johannes Gutenberg)", "year": 1440}
]

def initialize_game():
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_event' not in st.session_state:
        st.session_state.current_event = random.choice(HISTORICAL_EVENTS)
    if 'answered' not in st.session_state:
        st.session_state.answered = False
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ""

def next_question():
    st.session_state.current_event = random.choice(HISTORICAL_EVENTS)
    st.session_state.answered = False
    st.session_state.feedback = ""

# --- UI SETUP ---
st.set_page_config(page_title="History Hitster", page_icon="⏳")
initialize_game()

# Sidebar
with st.sidebar:
    st.title("📜 Anleitung")
    st.write("""
    1. Schätze das Jahr des Ereignisses.
    2. Gib deine Schätzung ein.
    3. Erhalte Punkte für Präzision!
    """)
    st.markdown("---")
    st.metric("Dein Score", st.session_state.score)
    if st.button("Spiel zurücksetzen"):
        st.session_state.score = 0
        next_question()
        st.rerun()

# Hauptbereich
st.title("⏳ History Hitster")
st.subheader("Wann passierte dieses Ereignis?")

event = st.session_state.current_event
st.info(f"### Ereignis: **{event['event']}**")

# Eingabe-Bereich
if not st.session_state.answered:
    user_guess = st.number_input("Gib das Jahr ein (nutze Minus für v. Chr.):", value=2000, step=1)
    
    if st.button("Antwort prüfen"):
        st.session_state.answered = True
        correct_year = event['year']
        diff = abs(user_guess - correct_year)
        
        if diff == 0:
            st.session_state.feedback = "PERFEKT! 🎯 Genau getroffen (+10 Punkte)"
            st.session_state.score += 10
        elif diff <= 5:
            st.session_state.feedback = f"Fast! Nur {diff} Jahre daneben. (+5 Punkte). Es war {correct_year}."
            st.session_state.score += 5
        elif diff <= 20:
            st.session_state.feedback = f"Gute Schätzung! {diff} Jahre Differenz. (+2 Punkte). Es war {correct_year}."
            st.session_state.score += 2
        else:
            st.session_state.feedback = f"Leider weit daneben. Es war {correct_year}. (0 Punkte)"
        
        st.rerun()

# Feedback-Anzeige
if st.session_state.answered:
    if "PERFEKT" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    elif "+" in st.session_state.feedback:
        st.warning(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)
        
    if st.button("Nächstes Ereignis ➡️"):
        next_question()
        st.rerun()

# Level-Anzeige basierend auf Score
st.markdown("---")
level = st.session_state.score // 20
st.write(f"**Aktuelles Level: {level}** 🎖️")
