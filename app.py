import streamlit as st
import openai
import os
import pickle
from dotenv import load_dotenv,find_dotenv
from PyPDF2 import PdfReader
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

# Sidebar contents
with st.sidebar:
    st.title('Common questions asked for safety:')

    # Path to your image file
    image_path = "Safe.jpg"

    # Display the image
    st.image(image_path, caption='Your safety,Our Priority ', use_column_width=True)
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model

    Built by [Winfry Nyarangi]
    ''')


    add_vertical_space(5)


# Load environment variables from a .env file if present
_ = load_dotenv(find_dotenv())
   
# Retrieve the OpenAI API key from the environment
os.environ["OPENAI_API_KEY"] = "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"


openai.api_key = os.environ["OPENAI_API_KEY"]

DB_FAISS_PATH = 'vectorstore/db_faiss'


def main():
    st.header("Besafe AI Chatbot💬")

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

            embeddings = OpenAIEmbeddings()

            db = FAISS.from_documents(chunks, embeddings)
            db.save_local(DB_FAISS_PATH)

            # Extracting store name from the file path
            # store_name = os.path.splitext(os.path.basename(file_path))[0]
            # # st.write(f'{store_name}')

            # if os.path.exists(f"{store_name}.pkl"):
            #     with open(f"{store_name}.pkl", "rb") as f:
            #         VectorStore = pickle.load(f)
            # else:
            #     embeddings = OpenAIEmbeddings()
            #     VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            #     with open(f"{store_name}.pkl", "wb") as f:
            #         pickle.dump(VectorStore, f)


        # Initialize the chat messages history
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [{"role": "assistant", "content": "Hello. How can I help?"}]

        # Prompt for user input and save
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            docs = db.similarity_search(query=prompt, k=3)

        # display the existing chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # If last message is not from assistant, we need to generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            # Call LLM
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    llm = OpenAI()
                    chain = load_qa_chain(llm=llm, chain_type="stuff")
                    with get_openai_callback() as cb:
                        response = chain.run(input_documents=docs, question=prompt)

                    r = response
                    response = r
                    st.write(response)

            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)


if __name__ == "__main__":
    main()

