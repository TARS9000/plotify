import streamlit as st
from PIL import Image
from style import get_css
import time
import requests
import yake
import requests
from io import BytesIO
import re

import replicate
from dotenv import load_dotenv, find_dotenv
import os


# api to return text summary
def get_image_api(prompt):
    prompt = f'{output_topics}, realistic, digital illustration, no text, in the style of Roald Dahl'
    envpath = find_dotenv()
    load_dotenv(envpath)
    replicate.Client()
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("0827b64897df7b6e8c04625167bbb275b9db0f14ab09e2454b9824141963c966")
    image_url = version.predict(prompt=prompt)
    print(image_url)
    print(image_url[0])
    return image_url



# function to return text keywords
def get_keywords():
    kw_extractor = yake.KeywordExtractor()
    text = output
    language = "en"
    max_ngram_size = 1
    deduplication_threshold = 0.25
    numOfKeywords = 7
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None, stopwords=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    keyword_list = [x[0] for x in keywords]

    return keyword_list


# api to get images based on keywords
def get_text_api():

    url = "https://plotifymodel-b4p33xwhra-ez.a.run.app/generate_summary?"

    param = {'genre': input3,
                'prompt': input1,
                'max_length': 200}

    x = requests.get(url, params=param).json()
    # print('get text api works')
    return x['generate_summary'][0]['generated_text'].split('|>',1)[1]


# function to display images
def display_image(image_url):
  # Make a GET request to the URL to retrieve the image data
  response = requests.get(image_url[0])

  # Create an image object from the image data
  image = Image.open(BytesIO(response.content))

  # Display the image
#   print('display image works')
  return image





## SITE CONFIG

# set the config for the page. App themes in .streamlit/config.toml
st.set_page_config(
            page_title="Plotify - create your story", # => Quick reference - Streamlit
            page_icon="streamlit_assets/plotify_logo_small.png",
            layout="wide", # wide
            initial_sidebar_state="expanded") # collapsed


st.markdown(get_css(), unsafe_allow_html=True)



## SIDEBAR

# Assets: Logo + headertext(plotify - create your story)
with st.sidebar.container():
    image = Image.open("streamlit_assets/plotify_logocomplete.png")
    st.image(image, use_column_width=True) #, caption ='Plotify - create your story'


# User Input Generic: Start API to return story with no prompts
with st.sidebar.form("no_user_input_form"):
    submitted_lucky = st.sidebar.button("I'M FEELING LUCKY")



## User Input with prompts and selections:
with st.sidebar.form("user_input_form"):

    # Input 1: Text Box: prompt to input short text, limit
    input1 = st.text_area('got the start of an idea?', height=150, max_chars = 1000)

    # Input 2: Radio buttons: choose genre
    input2 = st.radio('select your genre:',
                        ('Action 🤯',
                        'Comedy 🤣',
                        'Crime 👮🏽‍♀️',
                        'Drama 🎭',
                        'Fantasy 🚀',
                        'Horror 👻',
                        'Mystery 😵‍💫',
                        'Romance 😘',
                        'Young Adult 😎'))

    genre_dict = {'Action 🤯': 'action',
              'Comedy 🤣': 'comedy',
              'Crime 👮🏽‍♀️': 'crime',
              'Drama 🎭': 'novel',
              'Fantasy 🚀': 'fantasy' ,
              'Horror 👻': 'horror',
              'Mystery 😵‍💫': 'mystery',
              'Romance 😘': 'romance',
              'Young Adult 😎': 'childrens literature'}

    if input2:
        input3 = genre_dict.get(input2)

    # Button 2: Start API to return story with prompts + genre
    submitted_inputs = st.form_submit_button("GENERATE ME A STORY...")



## MAIN BODY

# Assets: borders top, right and bottom
# Assets: Headertext (your plotify-board)
image = Image.open("streamlit_assets/plotify_pageheadertext.png")
st.image(image,  use_column_width=None)



# Output 1: Summary Text
st.markdown(''' # ''')


with st.container():

    # button with inputs selected
    if submitted_inputs:
        # calls the first api to generate the output text
        with st.spinner("hold the pen, we're doing some plotting..."):
            output = get_text_api()
            if output:
                st.markdown(''' ##### your plotify story:  ''')
                st.write(output)
            else:
                st.error("Hmm, i'm stumped for a plot, awks!😬")

        st.markdown(''' # ''')

        # generates two more columns for keywords and image generation
        with st.container():
            col1, col2 = st.columns([1,4])

            # keyword generation
            with col1:
                if output:
                    st.markdown(''' ##### your plot keywords: ''')
                with col2:
                    output_topics = get_keywords()
                    st.markdown(", ".join(output_topics))

            st.markdown(''' # ''')
            # image generation
            #with col2:
            if output:
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    col1.markdown("##### your plot images:")
                with st.spinner("just grabbing a little extra inspiration..."):
                    col2.image(display_image(get_image_api(output_topics)), width=200)
                    col3.image(display_image(get_image_api(output_topics)), width=200)
                    col4.image(display_image(get_image_api(output_topics)), width=200)


    # lucky button selected
    if submitted_lucky:
        input1 = ''
        input2 = ''

        # calls the first api to generate the output text
        with st.spinner("hold the pen, we're doing some plotting..."):
            output = get_text_api()
            if output:
                st.markdown(''' ##### your plotify story:  ''')
                st.write(output)
            else:
                st.error("Hmm, i'm stumped for a plot, awks!😬")

        st.markdown(''' # ''')

        # generates two more columns for keywords and image generation
        with st.container():
            col1, col2 = st.columns([1,4])

            # keyword generation
            with col1:
                if output:
                    st.markdown(''' ##### your plot keywords: ''')
                with col2:
                    output_topics = get_keywords()
                    st.markdown(", ".join(output_topics))

            st.markdown(''' # ''')
            # image generation
            #with col2:
            if output:
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    col1.markdown("##### your plot images:")
                with st.spinner("just grabbing a little extra inspiration..."):
                    col2.image(display_image(get_image_api(output_topics)), width=200)
                    col3.image(display_image(get_image_api(output_topics)), width=200)
                    col4.image(display_image(get_image_api(output_topics)), width=200)
