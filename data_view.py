import streamlit as st
from pathlib import Path

# Define image paths
image_dir = Path("pics")
game_images = {
    "Memory Match": image_dir / "mem1.png",
    "Word Puzzle": image_dir / "mem1.png",
    "Sudoku": image_dir / "mem1.png",
    "Trivia": image_dir / "mem1.png",
    "Card Game": image_dir / "mem1.png",
    "Chess": image_dir / "mem1.png",
    "Color Matching": image_dir / "mem1.png",
    "Maze Solver": image_dir / "mem1.png"
}

# Initialize selected games
if "selected_games" not in st.session_state:
    st.session_state.selected_games = list(game_images.keys())[:4]

st.title("📱 Game Hub")
st.subheader("Tap to Play")

# Display square image buttons with labels using columns
cols = st.columns(2)
for i, game in enumerate(st.session_state.selected_games):
    with cols[i % 2]:
        st.markdown("###", unsafe_allow_html=True)  # Space between buttons
        if st.button(game, key=game):
            st.write(f"You selected: {game}")
        st.image(str(game_images[game]), width=100)

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("Sign Out"):
        st.write("Signing out...")

    st.subheader("🎮 Customize Game Selection")
    st.write("Choose which games appear in the menu:")
    selected_games = st.multiselect("Available Games", game_images.keys(), default=st.session_state.selected_games)

    if st.button("💾 Save Preferences"):
        st.session_state.selected_games = selected_games
        st.write("Game preferences updated!")
        st.rerun()
