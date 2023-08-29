import streamlit as st
from utils.helpers import ColdMailing, PDFTextExtractor

extractor = PDFTextExtractor()
mailer = ColdMailing()


st.title("Cold Letter")
st.write("Cold Letter is a tool to help you write cold emails. It scrapes the web for information about a company or professor and generates a template for you to use.")
type = st.radio("What would you like to do?", ("Company", "Professor"))


st.header("Target Information")
target_name = st.text_input("Name", placeholder="Google")

st.header("Your Information")
name = st.text_input("Your Name", placeholder="John Doe")
requested_position = st.text_input("Requested Position", placeholder="Software Engineer")

st.header("Resume Upload")
resume = st.file_uploader("Upload your resume", type="pdf")

# Submit button

if st.button("Submit"):
    content = mailer.generate(target_name, name, extractor.extract(resume), type, requested_position)
    st.write(content)
    
