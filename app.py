import streamlit as st
from backend import get_vid_id, get_transcript, process_video
import os

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_notes" not in st.session_state:
    st.session_state.show_notes = False

st.set_page_config(page_title="TubeQuery", page_icon="▶", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f9f9f9; color: #000000; }
    .main-header { color: #cc0000 !important; font-weight: bold; font-size: 32px; padding: 10px 0; }
    .chat-bubble { background: white; padding: 15px; border-radius: 8px; border: 1px solid #eee; margin-bottom: 10px; color: #000000; }
    .user-msg { border-left: 4px solid #cc0000; }
    .bot-msg { border-left: 4px solid #000; }
    p, label, div { color: #000000 !important; }

    .stButton > button {
        background-color: #cc0000 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
    }
    .stButton > button:hover {
        background-color: #aa0000 !important;
        color: white !important;
    }

    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div style="color:#cc0000; font-weight:bold; font-size:24px;">TubeQuery</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#ffffff;">Home</div>', unsafe_allow_html=True)
    if st.button("My Summaries"):
        st.session_state.show_notes = not st.session_state.show_notes
    st.divider()
    st.markdown('<div style="color:#ffffff;">Settings</div>', unsafe_allow_html=True)

st.markdown('<div class="main-header">TUBEQUERY</div>', unsafe_allow_html=True)

url_input = st.text_input("Paste YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if url_input:
    vid = get_vid_id(url_input)
    if vid:
        if st.button("Analyze Video"):
            with st.spinner("Analyzing transcript..."):
                transcript = get_transcript(vid)
                if transcript:
                    st.session_state.qa_chain = process_video(vid, transcript)
                    st.success("Video Processed! Ask the AI anything.")
    else:
        st.error("Invalid YouTube URL.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Video Analysis")
    if url_input:
        st.video(url_input)
    else:
        st.info("Paste a link to get started.")

with col2:
    st.subheader("AI Intelligence Hub")
    if st.session_state.qa_chain:
        query = st.chat_input("Ask about this video...")
        if query:
            with st.spinner("Thinking..."):
                response = st.session_state.qa_chain.invoke(query)
                st.session_state.chat_history.append({"q": query, "a": response})

        for chat in reversed(st.session_state.chat_history):
            st.markdown(f'<div class="chat-bubble user-msg"><b>You:</b> {chat["q"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble bot-msg"><b>TubeQuery:</b> {chat["a"]}</div>', unsafe_allow_html=True)
    else:
        st.write("Analyze a video first to chat with the bot.")

if st.session_state.show_notes:
    st.divider()
    st.subheader("My Summaries / Notes")

    if os.path.exists("notes.txt"):
        with open("notes.txt", "r", encoding="utf-8") as f:
            existing_notes = f.read()
        if existing_notes.strip():
            st.markdown("**Saved Notes:**")
            st.text_area("", value=existing_notes, height=200, disabled=True, key="saved_notes")
            if st.button("Clear All Notes"):
                os.remove("notes.txt")
                st.success("Notes cleared!")
                st.rerun()
        else:
            st.info("No notes saved yet.")
    else:
        st.info("No notes saved yet.")

    st.markdown("**Add a new note:**")
    new_note = st.text_area("Write your note here...", height=100, key="new_note")
    if st.button("Save Note"):
        if new_note.strip():
            with open("notes.txt", "a", encoding="utf-8") as f:
                if url_input:
                    f.write(f"\n--- Video: {url_input} ---\n")
                f.write(f"{new_note}\n")
            st.success("Note saved!")
            st.rerun()
        else:
            st.warning("Write something before saving!")
