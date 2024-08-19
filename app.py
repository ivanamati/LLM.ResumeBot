import streamlit as st
import rag_resume_chatbot
from name_checker import name_checker

st.title("'IvyBot'")
st.markdown("### Ivana's Assistant")
st.markdown("""IvyBot is an AI assistant dedicated to assisting Ivana in her job search by providing recruiters 
            with relevant information, but also showing her developing skills employing newest AI technology.""")

company_name = st.sidebar.text_input('Company (recruiter) Name')
openai_api_key = st.sidebar.text_input('OpenAI API key')

if company_name:
    name_checker(company_name)

with st.form('my_form'):
  text = st.text_area('Enter the question about Ivana')
  submitted = st.form_submit_button('ask IvyBot')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if not company_name:
    st.warning('Please enter your name or company name', icon='⚠')
  if submitted and openai_api_key.startswith('sk-') and company_name: 
  #if submitted:
    response = rag_resume_chatbot.generate_answer(text, openai_api_key)
    st.info(response)
# st.info("Thank you for taking the time to chat with my AI assistant.")


st.sidebar.divider()
st.sidebar.markdown("##### How to contact Ivana:")
st.sidebar.info("✉️ ivanamati@gmail.com")

st.sidebar.markdown("##### Ivana's Coding Projects:")
st.sidebar.info("https://www.linkedin.com/in/ivanamaticphd/ (Projects Section)")
st.sidebar.info("https://github.com/ivanamati")
