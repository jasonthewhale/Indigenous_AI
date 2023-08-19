from streamlit_folium import st_folium
from story_generator import *
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import folium
import time


st.set_page_config(
    page_title="Yaama!",
    page_icon="🌏",
    initial_sidebar_state="expanded",
)
st.title("Indigenous Storyteller")

st.markdown('##')

st.subheader("QLD indigenous language map")
st.caption('Source: Queensland Government')

QLD_LOC = [-20.917574, 142.702789]

if 'cur_lang' not in st.session_state:
    st.session_state['cur_lang'] = ''
if 'cur_select' not in st.session_state:
    st.session_state['cur_select'] = ''
if 'cur_click' not in st.session_state:
    st.session_state['cur_click'] = ''
if 'pre_select' not in st.session_state:
    st.session_state['pre_select'] = ''
if 'pre_click' not in st.session_state:
    st.session_state['pre_click'] = ''

story = ''
clicked_language = ''
df_location = get_map_data()

with st.sidebar:
    title = st.title("Language Information")
    st.markdown('##')
    st.markdown('##')
    reference = st.empty()
    # st.video('https://player.vimeo.com/video/143704810')


m = folium.Map(location=QLD_LOC, zoom_start=5, scrollWheelZoom=False, tiles='CartoDB positron')

for _, row in df_location.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['size'],
        color=row['color'],
        popup=row['Language'],
        tooltip=row['Language']
    ).add_to(m)

def update_click_language(click_lang):
    st.session_state['pre_click'] = st.session_state['cur_click']
    st.session_state['cur_click'] = click_lang

clicked_language = st_folium(m, width=700, height=450, key="map")['last_object_clicked_tooltip']
update_click_language(clicked_language)


st.subheader('Story Generator')

def update_select_language(select_lang):
    st.session_state['pre_select'] = st.session_state['cur_select']
    st.session_state['cur_select'] = select_lang

# language_input = st.empty()
selected_language = st.selectbox(label="Select or search a language", options=df['Language'].unique())
update_select_language(selected_language)

if st.session_state['cur_select'] != st.session_state['cur_click']:
    if st.session_state['cur_select'] != st.session_state['pre_select']:
        st.session_state['cur_lang'] = st.session_state['cur_select']
    elif st.session_state['cur_click'] != st.session_state['pre_click']:
        st.session_state['cur_lang'] = st.session_state['cur_click']

if not st.session_state['cur_click']:
    reference.markdown('Please **:red[click]** a language on the map or **:green[select/search]** one in the dropdown menu')
else:
    df_language = get_language_df(st.session_state['cur_lang'])
    df_info = pd.DataFrame({
            'Language': df_language['Language'],
            'Pronunciation': df_language['Pronunciation'],
            'Introduction': df_language['Introduction'],
            'Locations': df_language['Locations'],
            'Synonyms': df_language['Synonyms'],
            'Common words': df_language['Common words'],
    }).reset_index(drop=True).transpose()
    df_info = df_info.rename(columns={0: 'Document'})
    reference.write(df_info)

generate = st.button("Generate")

if generate:
    language_index = get_language_index(st.session_state['cur_select'])

    _, cent_col, _ = st.columns(3)
    with cent_col:
        st.image(get_image(st.session_state['cur_select']), caption=df_language['Image attribution'].values[0].split(',')[0])
    info = search_language_for_info(st.session_state['cur_select'])
    story = tell_story(info)
    story = label_story(st.session_state['cur_select'], story)
    st.markdown(story)