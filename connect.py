import streamlit as st
import random
import uuid
import json
import os
from streamlit_elements import elements, mui, sync, event

# Define bubble labels
bubble_labels = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E']

# Function to ensure no overlapping bubbles
def generate_non_overlapping_bubbles(labels, width=500, height=500, radius=40):
    positions = {}
    attempts = 0
    max_attempts = 1000
    while len(positions) < len(labels) and attempts < max_attempts:
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        overlap = False
        for pos in positions.values():
            dx = x - pos['x']
            dy = y - pos['y']
            if (dx**2 + dy**2) < (radius * 2)**2:
                overlap = True
                break
        if not overlap:
            label = labels[len(positions)]
            positions[label] = {'x': x, 'y': y, 'id': str(uuid.uuid4())}
        attempts += 1
    return positions

# Initialize session state
if 'bubbles' not in st.session_state:
    st.session_state.bubbles = generate_non_overlapping_bubbles(bubble_labels)

if 'connections' not in st.session_state:
    st.session_state.connections = []

if 'selected' not in st.session_state:
    st.session_state.selected = None

# Function to save connections to JSON
def save_connections_to_json():
    json_data = [[a, b] for a, b in st.session_state.connections]
    with open("connections.json", "w") as f:
        json.dump(json_data, f, indent=2)

# Reset button
if st.button("Reset Connections"):
    st.session_state.connections = []
    st.session_state.selected = None
    save_connections_to_json()

st.title("Bubble Connector")

with elements("canvas"):
    with mui.Box(sx={"position": "relative", "width": 500, "height": 500, "border": "1px solid #ccc", "borderRadius": "10px"}):

        for label, bubble in st.session_state.bubbles.items():
            def make_on_click(label=label):
                def on_click():
                    if st.session_state.selected is None:
                        st.session_state.selected = label
                    else:
                        if st.session_state.selected != label:
                            st.session_state.connections.append((st.session_state.selected, label))
                            save_connections_to_json()
                        st.session_state.selected = None
                return on_click

            mui.Button(
                label,
                onClick=make_on_click(),
                sx={
                    "position": "absolute",
                    "left": bubble['x'],
                    "top": bubble['y'],
                    "minWidth": "40px",
                    "minHeight": "40px",
                    "borderRadius": "50%",
                    "backgroundColor": "#4dabf5",
                    "color": "white"
                }
            )

        # Draw connections
        for conn in st.session_state.connections:
            b1 = st.session_state.bubbles[conn[0]]
            b2 = st.session_state.bubbles[conn[1]]
            event.Line(
                x1=b1['x'] + 20,
                y1=b1['y'] + 20,
                x2=b2['x'] + 20,
                y2=b2['y'] + 20,
                color="red",
                width=2
            )