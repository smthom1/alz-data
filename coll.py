import streamlit as st
import random

# Initialize characters and grid
characters = ['A', 'B', 'C', 'D', 'E', '1', '2', '3', '4', '5']
grid_size = 5  # 5x2 grid

# Randomize character positions on first load
if "shuffled" not in st.session_state:
    st.session_state.shuffled = random.sample(characters, len(characters))

# Store selected tiles
if "selection" not in st.session_state:
    st.session_state.selection = []

# Store formed pairs
if "pairs" not in st.session_state:
    st.session_state.pairs = []

st.title("Character Tile Matcher")

# Display the grid
cols = st.columns(5)
for i, char in enumerate(st.session_state.shuffled):
    col = cols[i % 5]
    with col:
        if st.button(char, key=f"btn_{i}"):
            if len(st.session_state.selection) < 2:
                st.session_state.selection.append(char)

# Show pair if two tiles are selected
if len(st.session_state.selection) == 2:
    pair = tuple(st.session_state.selection)
    st.session_state.pairs.append(pair)
    st.session_state.selection = []
    
# Add a reset button
if st.button("Reset Game"):
    st.session_state.shuffled = random.sample(characters, len(characters))
    st.session_state.selection = []
    st.session_state.pairs = []
    st.rerun()

# Display all formed pairs
if st.session_state.pairs:
    st.subheader("Formed Pairs:")
    for idx, (a, b) in enumerate(st.session_state.pairs):
        st.write(f"{idx+1}. {a} - {b}")

