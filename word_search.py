import streamlit as st
import random
import string

# --- CONFIG ---
GRID_SIZE = 6
WORDS = ["BIRD", "CAMEL", "SNAKE", "MONKEY", "CAT"]
DIRECTIONS = ['horizontal', 'vertical', 'diagonal']

# --- SESSION STATE INIT ---
if "selected_tiles" not in st.session_state:
    st.session_state.selected_tiles = []

if "found_words" not in st.session_state:
    st.session_state.found_words = set()

@st.cache_data
def create_grid(size, words: tuple, directions: tuple):
    def generate_empty_grid(size):
        return [['' for _ in range(size)] for _ in range(size)]

    def place_word(grid, word, direction):
        placed = False
        while not placed:
            if direction == 'horizontal':
                row = random.randint(0, size - 1)
                col = random.randint(0, size - len(word))
                if all(grid[row][col + i] in ('', word[i]) for i in range(len(word))):
                    for i in range(len(word)):
                        grid[row][col + i] = word[i]
                    placed = True
            elif direction == 'vertical':
                row = random.randint(0, size - len(word))
                col = random.randint(0, size - 1)
                if all(grid[row + i][col] in ('', word[i]) for i in range(len(word))):
                    for i in range(len(word)):
                        grid[row + i][col] = word[i]
                    placed = True
            elif direction == 'diagonal':
                row = random.randint(0, size - len(word))
                col = random.randint(0, size - len(word))
                if all(grid[row + i][col + i] in ('', word[i]) for i in range(len(word))):
                    for i in range(len(word)):
                        grid[row + i][col + i] = word[i]
                    placed = True

    def fill_grid(grid):
        for i in range(size):
            for j in range(size):
                if grid[i][j] == '':
                    grid[i][j] = random.choice(string.ascii_uppercase)

    grid = generate_empty_grid(size)
    for word in words:
        place_word(grid, word, random.choice(directions))
    fill_grid(grid)
    return grid

# --- INIT GRID ---
if "grid" not in st.session_state:
    st.session_state.grid = create_grid(GRID_SIZE, tuple(WORDS), tuple(DIRECTIONS))
    st.session_state.words = WORDS

grid = st.session_state.grid

# --- STYLE ---
st.markdown("""
<style>
button[kind="secondary"] {
    width: 60px !important;
    height: 60px !important;
    padding: 0 !important;
    margin: 2px !important;
    font-size: 24px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# --- UI TITLE ---
st.title("🧩 Word Search — Big Clickable Tiles That Work")

# --- TILE GRID ---
for i in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE, gap="small")
    for j in range(GRID_SIZE):
        coord = (i, j)
        letter = grid[i][j]
        is_selected = coord in st.session_state.selected_tiles
        btn_label = f"**:blue[{letter}]**" if is_selected else f"**{letter}**"
        if cols[j].button(btn_label, key=f"tile_{i}_{j}"):
            if is_selected:
                st.session_state.selected_tiles.remove(coord)
            else:
                st.session_state.selected_tiles.append(coord)

# --- CURRENT WORD ---
selected_word = ''.join([grid[i][j] for i, j in st.session_state.selected_tiles])
st.markdown(f"### Selected: `{selected_word}`")

# --- ACTION BUTTONS IN A ROW ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Restart"):
        st.session_state.grid = create_grid(GRID_SIZE, tuple(WORDS), tuple(DIRECTIONS))
        st.session_state.words = WORDS
        st.session_state.selected_tiles = []
        st.session_state.found_words = set()

with col2:
    if st.button("🔁 Clear"):
        st.session_state.selected_tiles = []

with col3:
    if st.button("✅ Submit"):
        if selected_word in st.session_state.words:
            if selected_word not in st.session_state.found_words:
                st.success(f"🎉 Found **{selected_word}**!")
                st.session_state.found_words.add(selected_word)
            else:
                st.info("Already found it!")
        else:
            st.error("Not a valid word.")
        st.session_state.selected_tiles = []

# --- WORD LIST ---
st.markdown("### Words to Find:")
for word in st.session_state.words:
    if word in st.session_state.found_words:
        st.markdown(f"- ~~{word}~~ ✅")
    else:
        st.markdown(f"- {word}")
