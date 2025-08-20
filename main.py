import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import tempfile

st.title("📘 QuizifyAI")
st.subheader("Generate MCQs, QnA, Flashcards, or a Summary from your PDF")

# ===============================
# Helper Functions
# ===============================
def load_file(uploaded_file):
    if uploaded_file is not None:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        # Pass temp path to PyPDFLoader
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        return docs
    else:
        return None


def get_chunks(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)

def get_llm():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found. Please set it in your .env file.")
    
    return ChatGroq(
        temperature=0.1,
        groq_api_key=api_key,
        #llama-3.3-70b-versatile
        model_name="llama-3.3-70b-versatile"
    )

def generate_prompt(llm, mode, num_questions, difficulty, chunk_text):
    if mode == "QNA":
        prompt = f"""
        You are a knowledgeable teacher. Generate {num_questions} question-answer pairs from the text below.
        Requirements:
        - Questions should be {difficulty} level
        - Answers should be complete, concise, and accurate
        - Include only factual information from the text
        - The format should be:
         Each flashcard MUST follow this exact format:
                Q: <question>
                A: <answer>

                Q: <question>
                A: <answer>
        - Each question must start with "Q:" and each answer with "A:"
        - Each Q/A pair must be separated by a blank line
        Text:
        {chunk_text}
        """
    elif mode == "MCQS":
        prompt = f"""
        You are an educational content creator. Create {num_questions} multiple-choice questions.
        Requirements:
        - Questions should be {difficulty} level
        - Each question must have 4 options (A–D)
        - Clearly indicate the correct option
        - Do not number questions beyond sequential order (1, 2, 3...)
        Text:
        {chunk_text}
        """
    elif mode == "Flashcards":
        prompt = f"""
        You are an expert educator. Create {num_questions} flashcards from the text below.
        Requirements:
            - Difficulty: {difficulty} level
            - Each flashcard MUST follow this exact format:
                Q.1: <question>
                A: <one-line concise answer>

                Q.2: <question>
                A: <one-line concise answer>

                (continue sequentially as Q.3, Q.4, etc.)
            - Absolutely do NOT use "1.Q" or any other numbering style.
            - Answers must be strictly one line (no long explanations).
            - Do not skip numbers.
        Text:
        {chunk_text}
        """
    elif mode == "Summary":
        prompt = f"""
        You are an expert summarizer. Create a clear, concise summary.
        Text:
        {chunk_text}
        """
    else:
        raise ValueError("Invalid mode.")
    return llm.invoke(prompt)

def consolidated_result(llm, mode, num_questions, difficulty, chunks):
    output = []
    for chunk in chunks:
        result = generate_prompt(llm, mode, num_questions, difficulty, chunk.page_content)
        output.append(result)

    joined_outputs = [o.content for o in output]

    prompt = f"Here are {mode} generated from different chunks:\n\n{joined_outputs}\n\n"

    if mode in ["MCQS", "QNA", "Flashcards"]:
        prompt += f"- Ensure {difficulty} level\n"
        prompt += f"- Limit to {num_questions} items\n"
        prompt += "- Remove duplicates\n"
        #- Number sequentially\n
    elif mode == "Summary":
        prompt += "- Merge into a coherent concise summary\n"
    prompt += "Return only the final polished output."

    return llm.invoke(prompt).content

# ===============================
# Streamlit App
# ===============================
uploaded_file = st.file_uploader("📂 Upload a PDF file", type=["pdf"])

if uploaded_file:
    docs = load_file(uploaded_file)
    chunks = get_chunks(docs)
    llm = get_llm()

    mode = st.radio("Choose a mode:", ["QNA", "MCQS", "Flashcards", "Summary"])

    num_questions, difficulty = None, None
    if mode in ["QNA", "MCQS", "Flashcards"]:
        difficulty = st.selectbox("Select difficulty level:", ["Easy", "Medium", "Hard"])
        num_questions = st.number_input("Enter number of questions:", min_value=1, step=1, max_value=50)

    if st.button("🚀 Generate"):
        with st.spinner("Generating..."):
            result = consolidated_result(llm, mode, num_questions, difficulty, chunks)
        st.success("✅ Done!")
        st.text_area("Result:", result, height=400)
