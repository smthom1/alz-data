import streamlit as st
import numpy as np

# Maze legend:
# 0 = path
# 1 = wall
# 2 = player
# 3 = goal

# Define the maze layout
maze = np.array([
    [2, 0, 1, 0, 3],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0]
])

if "player_pos" not in st.session_state:
    st.session_state.player_pos = [0, 0]

# Display the maze
def display_maze():
    display = ""
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if [i, j] == st.session_state.player_pos:
                display += "🧍"
            elif maze[i, j] == 1:
                display += "⬛"
            elif maze[i, j] == 3:
                display += "🎯"
            else:
                display += "⬜"
        display += "\n"
    st.text(display)

# Move function
def move_player(dx, dy):
    x, y = st.session_state.player_pos
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < maze.shape[0] and 0 <= new_y < maze.shape[1]:
        if maze[new_x, new_y] != 1:
            st.session_state.player_pos = [new_x, new_y]

# UI
st.title("🧩 Streamlit Maze Game")
display_maze()

col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⬆️"):
        move_player(-1, 0)
with col1:
    if st.button("⬅️"):
        move_player(0, -1)
with col3:
    if st.button("➡️"):
        move_player(0, 1)
with col2:
    if st.button("⬇️"):
        move_player(1, 0)

# Check for win condition
if maze[st.session_state.player_pos[0], st.session_state.player_pos[1]] == 3:
    st.success("🎉 You've reached the goal!")
