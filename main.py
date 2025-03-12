import streamlit as st 
from scrape import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from parse import parse_with_ollama

# Custom styles for better UI
st.markdown("""
    <style>
    .stChatMessage {
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Smart Scraper Chat")
st.markdown("Chat with the AI to extract and analyze web content!")

# Store session variables for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dom_content" not in st.session_state:
    st.session_state.dom_content = None

# Website Input and Scraping
url = st.text_input("🌐 Enter a Website URL:")

if st.button("🔍 Scrape Page"):
    if url:
        with st.spinner("Scraping the page... ⏳"):
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            st.session_state.dom_content = cleaned_content
        
        st.success("✅ Page scraping completed!")
        with st.expander("📜 View Scraped Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
        st.session_state.messages.append({"role": "ai", "content": "Scraping complete! Ask me anything about the page."})
    else:
        st.warning("⚠️ Please enter a valid URL.")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if st.session_state.dom_content:
    user_question = st.chat_input("💬 Type your question here...")

    if user_question:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})

        # Process and generate AI response
        with st.spinner("Thinking... 🤔"):
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, user_question)

        # Add AI response to chat history
        st.session_state.messages.append({"role": "ai", "content": result})

        # Display latest messages
        with st.chat_message("user"):
            st.markdown(user_question)
        with st.chat_message("ai"):
            st.markdown(result)
