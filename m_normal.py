import streamlit as st

# Define all available games with colorful icons
all_games = {
    "Memory Match": "🧠",
    "Word Puzzle": "📝",
    "Sudoku": "🔢",
    "Trivia": "❓",
    "Card Game": "🃏",
    "Chess": "♟️",
    "Color Matching": "🎨",
    "Maze Solver": "🚶‍♂️"
}

# Session state for tracking selected games
if "selected_games" not in st.session_state:
    st.session_state.selected_games = list(all_games.keys())[:4]  # Default to first 4 games

# Game menu layout
st.title("📱 Game Hub")
st.subheader("Tap to Play")

# Create a grid layout for games
cols = st.columns(2)
for i, game in enumerate(st.session_state.selected_games):
    with cols[i % 2]:
        if st.button(f"{all_games[game]} {game}", key=game):
            st.write(f"You selected: {game}")

# Settings menu with a full game list
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("Sign Out"):
        st.write("Signing out...")

    st.subheader("🎮 Customize Game Selection")
    st.write("Choose which games appear in the menu:")
    selected_games = st.multiselect("Available Games", all_games.keys(), default=st.session_state.selected_games)
    
    if st.button("💾 Save Preferences"):
        st.session_state.selected_games = selected_games
        st.write("Game preferences updated!")
        st.rerun()