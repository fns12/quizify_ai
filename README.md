# 📘 QuizifyAI

An interactive **Streamlit app** powered by **LangChain** and **Groq LLMs** that helps students learn faster by turning PDF study material into:

* **Q\&A (Question–Answer pairs)**
* **MCQs (Multiple-Choice Questions)**
* **Flashcards**
* **Summaries**

Upload your PDF, select a mode, and generate high-quality study content instantly.

---

## 🚀 Features

* 📂 **Upload PDFs** and automatically split them into manageable chunks.
* 🤖 **LLM-powered generation** using Groq’s `llama-3.3-70b-versatile` model.
* 📝 **Modes Available**:

  * Q\&A pairs
  * MCQs with answers
  * Flashcards (concise one-line answers)
  * Summaries
* 🎚️ **Difficulty Levels**: Easy, Medium, Hard
* ⏱️ **Fast & Accurate** generation with duplicate removal and consolidation.

---

## 🛠️ Installation & Running

## 🔑 Setting up Groq API Key

For this project, you need a **Groq API key**.

1. Sign up at [Groq](https://console.groq.com/) and get your API key.
2. Create a `.env` file in the root folder and add:

```bash
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### 1. Clone the repo

```bash
git clone https://github.com/fns12/quizify-ai.git
cd quizify-ai
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. Run the app with Streamlit:

```bash
streamlit run main.py
```
---
## 🚀 Using the Live Demo

You can try the deployed app here: **[Live Demo](https://quizify-ai12.streamlit.app/)**

When running the demo, you need to provide your **GROQ API Key**:

  1. Go to manage app,click the **three dots (⋮)** → **Settings** → **Secrets**.
  2. Add your key in the following format:

     ```
     GROQ_API_KEY="your_api_key_here"
     ```
  3. Save and restart the app.

---

## ▶️ Usage

1. Upload a **PDF file**.
2. Choose a **mode** (QNA, MCQs, Flashcards, or Summary).
3. Select **difficulty** and number of questions.
4. Click **Generate** 🚀.
5. View and copy results directly.

---

## 📂 Project Structure

```
quizify-ai/
│── main.py              # Main Streamlit app
│── requirements.txt    # Python dependencies
│── .env.example        # Example env file (ignored in git)
│── README.md           # Project documentation
```

---

## 📸 Screenshots (Optional)

*Add screenshots here of the interface and output.*

---

## 📌 Example Outputs

### Q\&A

```
Q.1: What is machine learning?  
A: Machine learning is a field of AI focused on training algorithms to learn patterns from data.  

Q.2: Define supervised learning.  
A: Supervised learning is a type of ML where models are trained on labeled data.  
```

### MCQ

```
1. Which of the following is a supervised algorithm?  
   A) K-Means  
   B) Linear Regression ✅  
   C) PCA  
   D) Autoencoder  
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

MIT License



 
