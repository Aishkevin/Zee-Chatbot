import streamlit as st
from groq import Groq
import random

# ---------------------------
# 🔑 API KEY (PUT YOUR KEY HERE)
# ---------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------------------
# NICKNAMES
# ---------------------------
NICKNAMES = ["Zee", "Berry", "Fishy", "Bro", "Zeeboy"]

def get_nickname():
    return random.choice(NICKNAMES)

# ---------------------------
# LOAD PERSONALITY
# ---------------------------
def load_personality():
    try:
        with open("Aishu.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "You are a chill, funny best friend AI."

personality = load_personality()

# ---------------------------
# UI
# ---------------------------
st.set_page_config(page_title="Berry AI Chat 💙", page_icon="💬")
st.title("💬 Chat with Berry AI 💙")

mode = st.radio(
    "Choose response mode:",
    ["Short 💬", "Detailed 📖"],
    horizontal=True
)

# ---------------------------
# MEMORY
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "nickname" not in st.session_state:
    st.session_state.nickname = get_nickname()

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# INPUT
# ---------------------------
user_input = st.chat_input("Talk to Berry...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        if mode == "Short 💬":
            length_rule = "Reply in 1–3 short lines. Keep it crisp and fun."
        else:
            length_rule = "Give detailed but fun and casual responses."

        nickname = st.session_state.nickname

        system_prompt = f"""
You are Aishu 💙, a chill, funny best-friend AI talking to "{nickname}".

Personality:
{personality}

Rules:
- Use nicknames like Zee, Berry, Bro naturally
- Be funny, casual, supportive
- Use emojis lightly 😎
- {length_rule}
- Never sound robotic
"""

        messages = [
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.9
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        bot_reply = f"Error 😅: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})