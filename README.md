# youtube_rag
This project allows you to ask questions about the content of any YouTube video using its transcript. It uses:

1. LangChain for building the pipeline
2. FAISS for semantic search over transcript chunks
3. Ollama to run local LLMs (like TinyLlama)
4. YouTube Transcript API for fetching transcripts


## Features

1. Extracts transcript from any public YouTube video
2. Splits and stores transcript using FAISS vector store
3. Embeds using mxbai-embed-large via Ollama
4. Answers using tinyllama (or other local LLMs)
5. Answers only based on the transcript context

🛠️ Installation

1. Clone the repository
```
git clone https://github.com/your-username/youtube-qa-langchain.git
cd youtube-qa-langchain
```
2. Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```
3. Install dependencies

```
pip install -r requirements.txt
```
4. Make sure Ollama is installed and running locally:
```
Install Ollama
```

5. Pull the required models
```
ollama pull mxbai-embed-large
ollama pull tinyllama
```
# Usage

Run the script:

```
python app.py
```
You'll be prompted to:
```
Enter a YouTube Video ID (e.g., dQw4w9WgXcQ)
Ask a question related to the video
```
# Example
```
Please enter Youtube Video ID: VbZ9_C4-Qbo
Ask your question related to the video: What is the speaker's main argument?
Answer: The speaker argues that AI can be aligned through human feedback, but highlights challenges in value alignment.
```
