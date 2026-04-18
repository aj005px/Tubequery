from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_vid_id(url):
    parsed = urlparse(url)
    return parse_qs(parsed.query).get("v", [None])[0] #getting Vid id for transcript

def get_transcript(vid):
    api = YouTubeTranscriptApi()
    transcript_list = api.list(vid)
    try:
        transcript = transcript_list.find_transcript(["en"])
    except:
        try:
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )
            transcript = transcript.translate("en")
        except:
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )
    return transcript.fetch()

def process_video(vid, transcript):
    texts = [line.text for line in transcript]
    vid_joined = " ".join(texts)

    #Adding yt video id to a document for RAG
    with open("youtube_transcripts.txt", "w", encoding="utf-8") as f:
        f.write(f"VIDEO ID: {vid}\n\n")
        f.write(vid_joined)

    #Adding chunks
    loader = TextLoader("youtube_transcripts.txt", encoding="utf-8")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = splitter.split_documents(documents)

    #Adding chunks to ChromaDB
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=GEMINI_API_KEY)
    vector_store = Chroma.from_documents(documents=splits, embedding=embeddings, collection_name="ipl_docs")

    #retriver
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY, temperature=0.3)

    prompt = PromptTemplate.from_template("""Use the following transcript context to answer the question.
Context: {context}
Question: {question}""")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    qa_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return qa_chain
