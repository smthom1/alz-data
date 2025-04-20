import streamlit as st
import numpy as np

# Initial puzzle (0 means empty)
puzzle = [
    [5, 0, 4, 0, 7, 0, 0, 1, 2],
    [0, 7, 0, 1, 0, 5, 3, 4, 0],
    [1, 0, 8, 0, 4, 2, 0, 6, 7],
    [8, 5, 9, 7, 6, 0, 4, 2, 0],
    [4, 2, 0, 8, 0, 3, 7, 9, 0],
    [7, 1, 0, 9, 2, 4, 8, 0, 6],
    [0, 6, 1, 5, 3, 7, 2, 0, 0],
    [2, 0, 7, 4, 0, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 0, 0, 7, 0]
]

# The correct solution (used for validation and hints)
solution = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

st.set_page_config(page_title="Sudoku")
st.title("Sudoku Game")

st.markdown("""
<style>
/* Pre-filled values (disabled) — gray background, gray text */
div[data-testid="column"] > div > input:disabled {
    background-color: #eee !important;
    color: #666 !important;
    font-weight: bold;
}

/* User-entered values — white background, black text */
div[data-testid="column"] > div > input:not(:disabled) {
    background-color: #fff !important;
    color: #000 !important;
    font-weight: bold;
    border: 1px solid #999;
    text-align: center;
    font-size: 20px;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# Session state setup
if "user_board" not in st.session_state:
    st.session_state.user_board = np.array(puzzle)
if "revealed" not in st.session_state:
    st.session_state.revealed = set()

def render_board():
    for i in range(9):
        cols = st.columns(9, gap="small")
        for j in range(9):
            key = f"cell_{i}_{j}"
            val = st.session_state.user_board[i][j]
            readonly = (puzzle[i][j] != 0) or ((i, j) in st.session_state.revealed)

            if readonly:
                cols[j].text_input("", value=str(solution[i][j]), disabled=True, key=key, label_visibility="collapsed")
            else:
                input_val = cols[j].text_input("", value=str(val) if val != 0 else "", max_chars=1, key=key, label_visibility="collapsed")
                if input_val.isdigit() and 1 <= int(input_val) <= 9:
                    st.session_state.user_board[i][j] = int(input_val)
                else:
                    st.session_state.user_board[i][j] = 0

def is_valid_solution(board):
    for i in range(9):
        row = board[i, :]
        col = board[:, i]
        box = board[(i//3)*3:(i//3)*3+3, (i%3)*3:(i%3)*3+3].flatten()
        if len(set(row)) != 9 or len(set(col)) != 9 or len(set(box)) != 9:
            return False
    return True

render_board()

# --- Buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Check Solution"):
        if np.any(st.session_state.user_board == 0):
            st.warning("⚠️ Please fill all cells before checking!")
        elif is_valid_solution(st.session_state.user_board):
            st.success("🎉 Congratulations! Your solution is correct!")
        else:
            st.error("❌ Sorry, the solution is not valid. Try again!")

with col2:
    if st.button("💡 Hint"):
        for i in range(9):
            for j in range(9):
                if st.session_state.user_board[i][j] != solution[i][j]:
                    st.session_state.user_board[i][j] = solution[i][j]
                    st.session_state.revealed.add((i, j))
                    st.experimental_rerun()

if st.button("Go to Game Hub for cognitively impaired"):
            st.markdown("""
                <meta http-equiv="refresh" content="2;url=/m_impaired" />
            """, unsafe_allow_html=True)

if st.button("Go to Game Hub for cognitively normal"):
            st.markdown("""
                <meta http-equiv="refresh" content="2;url=/m_normal" />
            """, unsafe_allow_html=True)