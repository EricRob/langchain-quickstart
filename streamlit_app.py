import streamlit as st
from langchain.llms import OpenAI
st.set_page_config(page_title="Anki Automatoton")
st.title('Anki Automatoton')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.info(llm(input_text))

col1, col2 = st.columns(2)

with col1:
    med_text = st.text_input("Source Text")

with col2:
    inst_text = st.text_input("Instruction Text")

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter the OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(text)
