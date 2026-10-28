# 🦆 Mini Rubber Ducky

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mini-rubber-ducky-mhz.streamlit.app/)

> 🌐 **Live Demo:** [https://mini-rubber-ducky-mhz.streamlit.app/](https://mini-rubber-ducky-mhz.streamlit.app/)

An interactive **Retrieval-Augmented Generation (RAG)** assistant built with **Streamlit** and the **Google GenAI SDK**. Mini Rubber Ducky answers complex questions about **Multimodal RAG** by querying a dedicated **Gemini File Search Store**, ensuring accurate, grounded answers directly from your source documents.

---

## ✨ Features

- **Grounded RAG**: Responses are strictly anchored to documents indexed in the Gemini File Search Store, avoiding hallucinations.
- **Multimodal RAG Knowledge**: Ready to discuss CLIP embeddings, Whisper audio transcription, contrastive learning, chunking, and multimodal architectures.
- **Clean Streamlit UI**: Chat interface with message history persistence, responsive layout, and conversation reset functionality.
- **Flexible Configuration**: Automatic fallback mechanism checking environment variables (`.env`) and Streamlit secrets (`st.secrets`).
- **Jupyter Notebook Workflow**: Includes `Starter File - RAG with Gemini File Search.ipynb` to create stores, batch upload, and index documents.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM**: Google Gemini (`gemini-3.5-flash-lite`)
- **SDK**: [Google GenAI Python SDK](https://github.com/google-gemini/generative-ai-python) (`google-genai`)
- **Embeddings**: `models/gemini-embedding-2` via Gemini File Search Store
- **Environment Management**: `python-dotenv`

---

## 📁 Project Structure

```text
Mini Rubber Ducky/
├── app.py                                         # Main Streamlit web application
├── Starter File - RAG with Gemini File Search.ipynb # Notebook for indexing & querying store
├── requirements.txt                               # Project dependencies
├── .env.example                                   # Sample environment variables
├── .gitignore                                     # Git ignore configuration
└── README.md                                      # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+ installed
- A Google Gemini API key ([Google AI Studio](https://aistudio.google.com/))

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/mini-rubber-ducky.git
cd "mini-rubber-ducky"
```

### 3. Create & Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
copy .env.example .env     # Windows
cp .env.example .env       # macOS / Linux
```

Fill in your credentials inside `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_FILE_SEARCH_STORE_NAME=fileSearchStores/your-store-id-here
```

> **Note:** If you haven't created a File Search Store yet, see the [Creating the File Search Store](#-creating-the-file-search-store) section below.

---

## 🖥️ Running the Application

Launch the Streamlit app:

```bash
streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

---

## 📓 Creating the File Search Store

To create a new store and index your documents:

1. Open `Starter File - RAG with Gemini File Search.ipynb` in VS Code, Cursor, or Google Colab.
2. Configure your `GEMINI_API_KEY`.
3. Create the store and upload documents:
   ```python
   from google import genai

   client = genai.Client()
   file_search_store = client.file_search_stores.create(
       config={
           "display_name": "mini rubber ducky",
           "embedding_model": "models/gemini-embedding-2"
       }
   )
   print(file_search_store.name)  # Use this name in your .env
   ```
4. Copy the resulting store name (`fileSearchStores/mini-rubber-ducky-...`) to `GEMINI_FILE_SEARCH_STORE_NAME` in your `.env`.

---

## ☁️ Deployment (Streamlit Community Cloud)

The application is deployed live on Streamlit Community Cloud:
👉 **[mini-rubber-ducky-mhz.streamlit.app](https://mini-rubber-ducky-mhz.streamlit.app/)**

When deploying your own fork to [Streamlit Community Cloud](https://streamlit.io/cloud):

Add your secrets in the app settings under **Secrets**:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
GEMINI_FILE_SEARCH_STORE_NAME = "fileSearchStores/your-store-id-here"
```

`app.py` is preconfigured to automatically fall back to `st.secrets` when `.env` is not present.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
