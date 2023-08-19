import streamlit as st
import threading
import numpy as np
import pandas as pd
import time
import asyncio
from story_generator import main

# st.text_input("Your name", key="name")

# # You can access the value at any point with:
# st.session_state.name



# # Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#   # Update the progress bar with each iteration.
#   latest_iteration.text(f'Generating story {i+1}%')
#   bar.progress(i + 1)
#   time.sleep(0.05)

# '...and now we\'re done!'



# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )

story = None


async def tell_story():
    await asyncio.sleep(5)
    story = "story"

async def show_progress():
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    percent_complete = 0

    for percent_complete in range(100):
        if story is not None:
            break
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.progress(100, text=progress_text)


async def main():
    await asyncio.gather(tell_story(), show_progress())

asyncio.run(main())