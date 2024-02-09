import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os

# Sidebar contents
with st.sidebar:
    st.title('Your Safety Guide:')
  
    # Path to your image file
    image_path = "Safe.jpg"

    # Display the image
    st.image(image_path, caption='Helping You Navigate your Safety ', use_column_width=True)
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model
                
   
    ''')


    add_vertical_space(5)
# Load environment variables from a .env file if present
load_dotenv()

# Retrieve the OpenAI API key from the environment
import os

# Set the environment variable
os.environ["OPENAI_API_KEY"] = "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"


openai_api_key = os.getenv('OPEN_API_KEY')

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"


def main():
    st.header("Safety Chatbot💬")

    # Get the file path from the user
    file_path = "BeSafeAI-Dataset.pdf"

    # Check if a file path is provided
    if file_path:
        # Open the PDF file
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)

            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)

            # Extracting store name from the file path
            store_name = os.path.splitext(os.path.basename(file_path))[0]
            # st.write(f'{store_name}')

            if os.path.exists(f"{store_name}.pkl"):
                with open(f"{store_name}.pkl", "rb") as f:
                    VectorStore = pickle.load(f)
            else:
                embeddings = OpenAIEmbeddings()
                VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
                with open(f"{store_name}.pkl", "wb") as f:
                    pickle.dump(VectorStore, f)