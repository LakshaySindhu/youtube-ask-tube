import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from google import genai
import re

# --- Config ---
st.set_page_config(
    page_title="TubeAsk - YouTube Q&A",
    page_icon="🎥",
    layout="centered"
)

# --- Initialize Gemini Client ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- Helper: Extract Video ID ---
def extract_video_id(url):
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# --- Helper: Fetch Transcript (v1.2.4 compatible) ---
def get_transcript(video_id):
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id)
        full_text = " ".join([entry.text for entry in transcript])
        return full_text, None
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return None, "No transcript found for this video."
    except Exception as e:
        return None, str(e)

# --- Helper: Ask Gemini ---
def ask_gemini(transcript, question):
    prompt = f"""
    You are a helpful assistant. A user has watched a YouTube video and wants to ask questions about it.
    
    Here is the full transcript of the video:
    ---
    {transcript[:50000]}
    ---
    
    Answer the following question based ONLY on the transcript above.
    If the answer is not in the transcript, say "This topic wasn't covered in the video."
    Be clear, concise and helpful in your response.
    
    Question: {question}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# --- Helper: Auto Summarize ---
def summarize_video(transcript):
    prompt = f"""
    You are a helpful assistant. Summarize the following YouTube video transcript.
    
    Transcript:
    ---
    {transcript[:50000]}
    ---
    
    Provide:
    1. A 3-4 line overall summary
    2. 5 key points from the video
    3. Main takeaway or conclusion
    
    Keep it clear and concise.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# ---- UI Starts Here ----

st.title("🎥 TubeAsk")
st.markdown("Ask anything about any YouTube video using AI")
st.divider()

# --- URL Input + Button ---
url = st.text_input(
    "Paste YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="visible"
)

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    load_button = st.button("🚀 Load Video", use_container_width=True)

# --- Load Video on Button Click ---
if load_button:
    if not url:
        st.warning("⚠️ Please paste a YouTube URL first.")
    else:
        video_id = extract_video_id(url)

        if not video_id:
            st.error("❌ Invalid YouTube URL. Please check and try again.")
        else:
            # Store video_id
            st.session_state.pending_video_id = video_id

# --- Process Video if pending ---
if "pending_video_id" in st.session_state:
    video_id = st.session_state.pending_video_id

    # Show thumbnail
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            f"https://img.youtube.com/vi/{video_id}/0.jpg",
            use_container_width=True,
            caption="🎬 Video Preview"
        )

    # Fetch transcript only if new video
    if st.session_state.get("video_id") != video_id:
        with st.spinner("⏳ Fetching transcript... please wait"):
            transcript, error = get_transcript(video_id)

            if error:
                st.error(f"❌ {error}")
            else:
                st.session_state.transcript = transcript
                st.session_state.video_id = video_id
                st.session_state.messages = []
                st.session_state.show_transcript = False
                st.success(f"✅ Transcript loaded! ({len(transcript.split())} words)")
    else:
        st.success(f"✅ Transcript already loaded! ({len(st.session_state.transcript.split())} words)")

# --- Q&A Section ---
if "transcript" in st.session_state:

    st.divider()

    # --- Auto Summarize Button ---
    if st.button("⚡ Auto Summarize This Video", use_container_width=True):
        with st.spinner("Summarizing..."):
            summary = summarize_video(st.session_state.transcript)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"📋 **Video Summary**\n\n{summary}"
            })

    st.subheader("💬 Ask Anything About This Video")
    st.caption("Examples: 'What is the main topic?', 'List all tools mentioned', 'Explain the key concept simply'")

    # --- Display Chat History ---
    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Chat Input ---
    question = st.chat_input("Type your question here...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_gemini(st.session_state.transcript, question)
                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

    st.divider()

    # --- Bottom Buttons ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with col2:
        if st.button("📄 View Transcript", use_container_width=True):
            st.session_state.show_transcript = not st.session_state.get("show_transcript", False)

    if st.session_state.get("show_transcript", False):
        with st.expander("📄 Raw Transcript", expanded=True):
            st.write(st.session_state.transcript)

    # --- Load New Video Button ---
    st.divider()
    if st.button("🔄 Load a Different Video", use_container_width=True):
        for key in ["transcript", "video_id", "pending_video_id", "messages", "show_transcript"]:
            st.session_state.pop(key, None)
        st.rerun()

# --- Footer ---
st.divider()
st.markdown(
    "<center>Built using Streamlit & Gemini AI</center>",
    unsafe_allow_html=True
)