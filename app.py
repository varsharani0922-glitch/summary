import streamlit as st
import PyPDF2
import heapq
import re

# Page config
st.set_page_config(page_title="Summarizer", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>📄 Research Paper Summarizer</h1>", unsafe_allow_html=True)
st.write("Upload a research paper and generate bullet-point summary instantly.")

# Upload PDF
uploaded_file = st.file_uploader("📂 Upload PDF", type="pdf")

# Number of bullet points
num = st.number_input("Enter number of bullet points", min_value=1, step=1, value=5)

# Simple stopwords list (no NLTK)
stop_words = set([
    "the","is","in","and","to","of","a","that","it","on","for","as","with",
    "was","were","this","by","an","be","are","or","from","at","which","but"
])

# 🔹 Extract text
def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# 🔹 Summarize (no NLTK)
def summarize(text, n):
    text = re.sub(r'\s+', ' ', text)

    # Sentence split (simple)
    sentences = text.split('.')

    # Word frequency
    words = text.lower().split()
    word_freq = {}

    for word in words:
        word = re.sub(r'[^a-zA-Z0-9]', '', word)
        if word and word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

    if not word_freq:
        return []

    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq

    # Score sentences
    scores = {}
    for sent in sentences:
        for word in sent.lower().split():
            word = re.sub(r'[^a-zA-Z0-9]', '', word)
            if word in word_freq:
                scores[sent] = scores.get(sent, 0) + word_freq[word]

    n = min(n, len(scores))
    summary = heapq.nlargest(n, scores, key=scores.get)

    return summary

# 🔹 Generate summary
if st.button("🚀 Generate Summary"):
    if uploaded_file is not None:

        with st.spinner("Processing... ⏳"):
            text = extract_text(uploaded_file)
            result = summarize(text, int(num))

        st.success("✅ Summary Generated!")

        st.subheader("🔹 Summary:")
        summary_text = ""

        for i, line in enumerate(result, 1):
            st.write(f"{i}. {line.strip()}")
            summary_text += f"{i}. {line.strip()}\n"

        # Download summary
        st.download_button(
            label="📥 Download Summary",
            data=summary_text,
            file_name="summary.txt",
            mime="text/plain"
        )

    else:
        st.warning("⚠️ Please upload a PDF file")