import streamlit as st
import pymongo
from pymongo import MongoClient
import pandas as pd
import pdfplumber
import PyPDF2
from rake_nltk import Rake
import string
import io
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import lxml

country = st.sidebar.text_input('Country')
uploaded_file = st.file_uploader('Upload your resume')
file_text = ''
phrases = []

if uploaded_file is not None:
    uploaded_file.seek(0)
    file = uploaded_file.read()
    pdf = PyPDF2.PdfFileReader(io.BytesIO(file))
    
    for page in range(pdf.getNumPages()):
        file_text += (pdf.getPage(page).extractText())
        phrases.extend(keyphrases(file_text,2,4,10))
        
if len(phrases) > 0:
    q_terms = st.multiselect('Select key phrases',options=phrases,default=phrases)

def keyphrases(file,min_word,max_word,num_phrases):

    text = file
    text = text.lower()
    text = ''.join(s for s in text if ord(s)>31 and ord(s)<126)
    text = text
    text = re.sub(' +', ' ', text)
    text = text.translate(str.maketrans('', '',string.punctuation))
    text = ''.join([i for i in text if not i.isdigit()])
    r = Rake(min_length = min_word, max_length = max_word)
    r.extract_keywords_from_text(text)
    phrases = r.get_ranked_phrases()
    
    if num_phrases < len(phrases):
        phrases = phrases[0:num_phrases]
        
    return phrases    