import os
import json
from typing import Any

import requests
import streamlit as st

st.set_page_config(page_title="Resume RAG Chatbot", layout="centered")

st.title("📄 Resume RAG Chatbot")
st.markdown("Ask questions about my skills, projects, and experience.")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📎 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- **{s.get('source', s['id'])}** (score: {s.get('score', 'N/A')})")
                    st.code(s["text"], language="text")

if prompt := st.chat_input("Ask about my resume/portfolio..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            resp = requests.post(API_URL, json={"question": prompt}, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            answer = data.get("answer", "")
            sources = data.get("sources", [])
            message_placeholder.markdown(answer)
            if sources:
                with st.expander("📎 Sources"):
                    for s in sources:
                        st.markdown(f"- **{s.get('source', s['id'])}** (score: {s.get('score', 'N/A')})")
                        st.code(s.get("text", ""), language="text")
            st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
        except Exception as e:
            message_placeholder.error(f"❌ Error: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {e}"})
