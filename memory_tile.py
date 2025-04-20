import streamlit as st
import random
import time


EMOJIS = ['🍎', '🍌', '🍇', '🍓', '🍒', '🍍', '🥝', '🍉']
GRID_SIZE = 4


def init_game():
    tiles = EMOJIS * 2
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
            height: 100px;
            width: 100px;
            font-size: 64px !important;
            line-height: 100px !important;
            padding: 0 !important;
            margin: 2px !important;
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)


st.title("🧠 Memory Tile Game")
st.caption("Flip two cards. Mismatched cards flip back on the next click!")


for row in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for col in range(GRID_SIZE):
        idx = row * GRID_SIZE + col
        val = st.session_state.tiles[idx]

        if idx in st.session_state.matched or idx in st.session_state.flipped:
            cols[col].button(val, key=f"tile_{idx}", disabled=True)
        else:
            cols[col].button("❓", key=f"tile_{idx}", on_click=flip_tile, args=(idx,))


st.markdown(f"**Moves**: {st.session_state.moves}")
st.markdown(f"**Matches Found**: {st.session_state.matches_found} / 8")

if st.session_state.matches_found == 8:
    duration = int(time.time() - st.session_state.start_time)
    st.success(f"🎉 You won in {st.session_state.moves} moves and {duration} seconds!")
    if st.button("🔁 Play Again"):
        init_game()
        st.rerun()
