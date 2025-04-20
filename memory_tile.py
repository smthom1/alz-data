import streamlit as st
import random
import time


PICTURES = ["game_pictures/apple.jpeg", "game_pictures/banana.jpeg", "game_pictures/grapes.jpeg", "game_pictures/orange.jpeg", "game_pictures/pear.jpeg", "game_pictures/pomegranate.jpeg", "game_pictures/strawberry.jpeg", "game_pictures/plum.jpeg"]
GRID_SIZE = 4


def init_game():
    tiles = PICTURES * 2
    random.shuffle(tiles)
    st.session_state.tiles = tiles
    st.session_state.flipped = []
    st.session_state.matched = []
    st.session_state.moves = 0
    st.session_state.matches_found = 0
    st.session_state.start_time = time.time()

if 'tiles' not in st.session_state:
    init_game()

def flip_tile(idx):
    if idx in st.session_state.matched or idx in st.session_state.flipped:
        return


    if len(st.session_state.flipped) == 2:
        idx1, idx2 = st.session_state.flipped
        if st.session_state.tiles[idx1] != st.session_state.tiles[idx2]:
            st.session_state.flipped = []

    st.session_state.flipped.append(idx)

    # Check for match
    if len(st.session_state.flipped) == 2:
        idx1, idx2 = st.session_state.flipped
        val1, val2 = st.session_state.tiles[idx1], st.session_state.tiles[idx2]
        st.session_state.moves += 1
        if val1 == val2:
            st.session_state.matched.extend([idx1, idx2])
            st.session_state.flipped = []
            st.session_state.matches_found += 1


st.markdown("""
    <style>
        div[class^="stButton"] > button {
            height: 140px;
            width: 140px;
            font-size: 100px !important;
            line-height: 140px !important;
            padding: 0 !important;
            margin: 2px !important;
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Tile Game")
st.subheader("Find Each of the 8 Pairs of Fruit. Click on Two Tiles to Start Playing.")


for row in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for col in range(GRID_SIZE):
        idx = row * GRID_SIZE + col
        val = st.session_state.tiles[idx]

        from PIL import Image

        if idx in st.session_state.matched or idx in st.session_state.flipped:
            with open(val, "rb") as file:
                img = Image.open(file)
                cols[col].image(img, width=150)



        else:
            # Hidden tile
            cols[col].button("❓", key=f"tile_{idx}", on_click=flip_tile, args=(idx,))



st.markdown(
    f"<p style='font-size:32px; font-weight:600;'> Moves: {st.session_state.moves}</p>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='font-size:32px; font-weight:600;'> Matches Found: {st.session_state.matches_found} / 8</p>",
    unsafe_allow_html=True
)


if st.session_state.matches_found == 8:
    duration = int(time.time() - st.session_state.start_time)
    st.markdown(
    f"""
    <div style='
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #28a745;
        margin-top: 20px;
    '>
        <h2 style='font-size: 36px; color: #155724; margin: 0;'>
             You won in {st.session_state.moves} moves and {duration} seconds!
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown("""
    <style>
    .play-again-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    div.stButton > button {
        background-color: #28a745;
        color: white;
        padding: 14px 28px;
        font-size: 40px;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #218838;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="play-again-button">', unsafe_allow_html=True)
    if st.button("Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

