import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain import OpenAI, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain.llms import GooglePalm
import tempfile


st.set_page_config(layout="wide")

api_key="AIzaSyCGMc-kCuTWZ1qHUZ7WwVZ0aSPtrcAqt_I"
llm=GooglePalm(google_api_key=api_key,temperature=0.7)

@st.cache_resource

def summarize_pdf(pdf_file_path):    
        loader = PyPDFLoader(pdf_file_path)
        docs = loader.load_and_split()
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(docs)   
        return summary

def extract_text_from_pdf(file_path):
    # Open the PDF file using PyPDF2    
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        text = ""
        
        # Iterate through all the pages and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n"
    
    return text


st.subheader("Summarize Document")
input_file = st.file_uploader("Upload your document here", type=['pdf'])

if input_file is not None:
    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(input_file.read())
        temp_file_path = temp_file.name



if input_file is not None:
    if st.button("Summarize Document"):
        with open("doc_file.pdf", "wb") as f:
            f.write(input_file.getbuffer())
            
        col1, col2 = st.columns([1,1])
        with col1:
            st.info("File uploaded successfully")
            extracted_text = extract_text_from_pdf("doc_file.pdf")
            st.markdown("**Extracted Text is Below:**")
            st.info(extracted_text)
        with col2:
            st.markdown("**Summary Result**")
            text = extract_text_from_pdf("doc_file.pdf")
            doc_summary = summarize_pdf(temp_file_path)
            st.success(doc_summary)
            