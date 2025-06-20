import streamlit as st
from app.core.embeddings import load_embeddings
from app.core.llm import load_llm
from app.core.pdf import process_pdf

def render():
    st.set_page_config(page_title="PDF RAG Assistant", layout="wide")
    st.title("PDF RAG Assistant")

    st.markdown("""
    **Ứng dụng AI giúp bạn hỏi đáp trực tiếp với nội dung tài liệu PDF bằng tiếng Việt**
    **Cách sử dụng đơn giản:**
    1. **Upload PDF** Chọn file PDF từ máy tính và nhấn "Xử lý PDF"
    2. **Đặt câu hỏi** Nhập câu hỏi về nội dung tài liệu và nhận câu trả lời ngay lập tức
    ---""")

    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if "models_loaded" not in st.session_state:
        st.session_state.models_loaded = False
    if "embeddings" not in st.session_state:
        st.session_state.embeddings = None
    if "llm" not in st.session_state:
        st.session_state.llm = None

    if not st.session_state.models_loaded:
        st.info("Đang tải models...")
        st.session_state.embeddings = load_embeddings()
        st.session_state.llm = load_llm()
        st.session_state.models_loaded = True
        st.success("Models đã sẵn sàng!")
        st.rerun()

    uploaded_file = st.file_uploader("Upload file PDF", type="pdf")
    if uploaded_file and st.button("Xử lý PDF"):
        with st.spinner("Đang xử lý..."):
            st.session_state.rag_chain, num_chunks = process_pdf(
                uploaded_file,
                st.session_state.embeddings,
                st.session_state.llm
            )
        st.success(f"Hoàn thành! {num_chunks} chunks")

    if st.session_state.rag_chain:
        question = st.text_input("Đặt câu hỏi:")
        if question:
            with st.spinner("Đang trả lời..."):
                output = st.session_state.rag_chain.invoke(question)
                answer = output.split("Answer:")[1].strip() if "Answer:" in output else output.strip()
                st.write("**Trả lời:**")
                st.write(answer)
                
                
def render2():
    st.set_page_config(page_title="Lem nhem", layout="wide")
    st.title("Lem's Slave AI")
    string = """
    **Ứng dụng AI giúp bạn hỏi đáp trực tiếp với nội dung tài liệu PDF**
    **Cách sử dụng đơn giản:**
    1. **Upload PDF** Chọn file PDF từ máy tính và nhấn "Xử lý PDF"
    2. **Đặt câu hỏi** Nhập câu hỏi về nội dung tài liệu và nhận câu trả lời ngay lập tức
    ---"""
    string.replace("bạn", "Lem")
    st.markdown(string)

    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if "models_loaded" not in st.session_state:
        st.session_state.models_loaded = False
    if "embeddings" not in st.session_state:
        st.session_state.embeddings = None
    if "llm" not in st.session_state:
        st.session_state.llm = None

    if not st.session_state.models_loaded:
        st.info("Đang tải models...")
        st.session_state.embeddings = load_embeddings()
        st.session_state.llm = load_llm()
        st.session_state.models_loaded = True
        st.success("Models đã sẵn sàng!")
        st.rerun()

    uploaded_file = st.file_uploader("Upload file PDF", type="pdf")
    if uploaded_file and st.button("Xử lý PDF"):
        with st.spinner("Đang xử lý..."):
            st.session_state.rag_chain, num_chunks = process_pdf(
                uploaded_file,
                st.session_state.embeddings,
                st.session_state.llm
            )
        st.success(f"Hoàn thành! {num_chunks} chunks")

    if st.session_state.rag_chain:
        question = st.text_input("Đặt câu hỏi:")
        if question:
            with st.spinner("Đang trả lời..."):
                output = st.session_state.rag_chain.invoke(question)
                answer = output.split("Answer:")[1].strip() if "Answer:" in output else output.strip()
                st.write("**Trả lời:**")
                st.write(answer)
                