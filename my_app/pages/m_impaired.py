import streamlit as st
from pathlib import Path
import base64

# Path to your images
image_dir = Path("pics")

# Define your games and image filenames
game_images = {
    "Memory Match": "mem1.png",
    "Word Puzzle": "mem1.png",
    "Sudoku": "mem1.png",
    "Trivia": "mem1.png",
    "Card Game": "mem1.png",
    "Chess": "mem1.png",
    "Color Matching": "mem1.png",
    "Maze Solver": "mem1.png"
}

# Helper to convert local image to base64 string
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load images
game_base64 = {
    name: img_to_base64(image_dir / filename)
    for name, filename in game_images.items()
}

# Initialize selected games
if "selected_games" not in st.session_state:
    st.session_state.selected_games = list(game_images.keys())[:2]

# Custom CSS
st.markdown("""
    <style>
    .img-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 12px;
        margin: 10px;
        background-color: #fff;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.2s ease-in-out;
        text-align: center;
    }
    .img-card:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    .img-card img {
        width: 120px;
        height: 120px;
        object-fit: cover;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    .img-label {
        font-size: 16px;
        font-weight: 500;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>📱 Game Hub</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Tap a Game to Play</h3><br>", unsafe_allow_html=True)

# Create dynamic grid
cols = st.columns(2)
for i, game in enumerate(st.session_state.selected_games):
    with cols[i % 2]:
        b64_img = game_base64[game]
        button_html = f"""
        <form action="" method="post">
            <button class="img-card" name="selected_game" value="{game}" type="submit">
                <img src="data:image/png;base64,{b64_img}" alt="{game}">
                <div class="img-label">{game}</div>
            </button>
        </form>
        """
        st.markdown(button_html, unsafe_allow_html=True)

# Handle game selection
selected_game = st.session_state.get("selected_game", None)
query_params = st.query_params

if selected_game:
    st.success(f"You selected: {selected_game}")
elif "selected_game" in query_params:
    st.session_state.selected_game = query_params["selected_game"][0]

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    if st.button("🔒 Sign Out"):
        st.warning("Signing out...")
        st.markdown("""
            <meta http-equiv="refresh" content="0;url=/" />
        """, unsafe_allow_html=True)

    st.markdown("### 🎮 Customize Game Selection")
    selected_games = st.multiselect("Available Games", game_images.keys(), default=st.session_state.selected_games)

    if st.button("💾 Save Preferences"):
        st.session_state.selected_games = selected_games
        st.rerun()
