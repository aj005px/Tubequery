# TubeQuery

A YouTube RAG (Retrieval Augmented Generation) chatbot that lets you ask questions about any YouTube video using its transcript.

## What it does

- Paste any YouTube URL and it fetches the transcript automatically
- Supports videos in any language, falls back to the available language if English is not found
- Chunks the transcript and stores it in a ChromaDB vector store
- Uses Groq (llama-3.3-70b) to answer questions based on the transcript
- Lets you save and manage notes for each video

## Tech Stack

- Python
- Streamlit (frontend)
- LangChain (RAG pipeline)
- ChromaDB (vector store)
- Google Gemini Embeddings
- Groq LLM
- Supadata API (YouTube transcript fetching)

## Project Structure

```
tubequery/
├── app.py               # Streamlit frontend
├── backend.py           # Core functions (transcript, RAG pipeline)
├── notes.txt            # Saved notes (auto-created)
├── .env                 # API keys (not pushed to git)
└── .gitignore
```

## Setup

1. Clone the repo

```
git clone https://github.com/yourusername/tubequery.git
cd tubequery
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys

```
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
SUPADATA_API_KEY=your_supadata_api_key
```

4. Run the app

```
streamlit run app.py
```

## Getting API Keys

- Gemini API: https://aistudio.google.com (free, 1500 requests/day)
- Groq API: https://console.groq.com (free tier available)
- Supadata API: https://supadata.ai (free, 100 requests/day) - used for fetching YouTube transcripts on cloud

## Notes

- The transcript file is overwritten each time a new video is analyzed
- Notes are saved in append mode to notes.txt and persist across sessions
- Works best with educational and tech videos that have auto-generated captions
