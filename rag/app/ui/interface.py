import streamlit as st
from app.core.embeddings import load_embeddings
from app.core.llm import load_llm
from app.core.pdf import process_pdf
import time

def clear_chat():
    """Xóa lịch sử chat"""
    st.session_state.chat_history = []
    

def display_chat():
    """Hiển thị lịch sử chat"""
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write("Xin chào! Tôi là AI assistant. Hãy upload file PDF và bắt đầu đặt câu hỏi về nội dung tài liệu nhé! 😊")

def add_message(role, content):
    """Thêm tin nhắn vào lịch sử chat"""
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "timestamp": time.time()
    })    


def render():
    st.set_page_config(page_title="PDF RAG Assistant", layout="wide")
    st.title("PDF RAG Assistant")

    st.logo("/kaggle/working/RAG/rag/app/image/logo.png", size="large")

    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if "models_loaded" not in st.session_state:
        st.session_state.models_loaded = False
    if "embeddings" not in st.session_state:
        st.session_state.embeddings = None
    if "llm" not in st.session_state:
        st.session_state.llm = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    if 'pdf_name' not in st.session_state:
        st.session_state.pdf_name = ""
        
    with st.sidebar:
        st.title("⚙️ Cài đặt")
        # Load models if not already loaded
        if not st.session_state.models_loaded:
            st.info("Đang tải models...")
            st.session_state.embeddings = load_embeddings()
            st.session_state.llm = load_llm()
            st.session_state.models_loaded = True
            st.success("Models đã sẵn sàng!")
            st.rerun()
        else:
            st.success("Models đã sẵn sàng!")
            
        st.markdown("---")
        
        # Upload PDF
        st.subheader("📄 Upload tài liệu")

        uploaded_file = st.file_uploader("Upload file PDF", type="pdf")
        if uploaded_file and st.button("🔄 Xử lý PDF", use_container_width=True):
            with st.spinner("Đang xử lý..."):
                st.session_state.rag_chain, num_chunks = process_pdf(
                    uploaded_file,
                    st.session_state.embeddings,
                    st.session_state.llm
                )
                st.session_state.pdf_processed = True
                st.session_state.pdf_name = uploaded_file.name
            st.success(f"Hoàn thành! {num_chunks} chunks")
            st.rerun()
            
        # PDF status
        if st.session_state.pdf_processed:
            st.success(f"📄 Đã tải: {st.session_state.pdf_name}")
        else:
            st.info("📄 Chưa có tài liệu")
            
        st.markdown("---")
        
        # Chat controls
        st.subheader("💬 Điều khiển Chat")
        if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
            clear_chat()
            st.rerun()
            
        st.markdown("---")
        
        # Instructions
        st.subheader("📋 Hướng dẫn")
        st.markdown("""
        **Cách sử dụng:**
        1. **Upload PDF** - Chọn file và nhấn "Xử lý PDF"
        2. **Đặt câu hỏi** - Nhập câu hỏi trong ô chat
        3. **Nhận trả lời** - AI sẽ trả lời dựa trên nội dung PDF
        """)
    
     # Main content
    st.markdown("*Trò chuyện với Chatbot để trao đổi về nội dung tài liệu PDF của bạn*")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        display_chat()
    # Chat input
    if st.session_state.models_loaded: 
        if st.session_state.pdf_processed:
            if st.session_state.rag_chain:
                question = st.text_input("Nhập câu hỏi của bạn...")
                if question:
                    # Add user message to chat history
                    add_message("user", question)
                    
                    # Display user message
                    with st.chat_message("user"):
                        st.write(question)
                        
                    # Generate response
                    with st.chat_message("assistant"):
                    
                        with st.spinner("Đang suy nghĩ..."):
                            try:
                                output = st.session_state.rag_chain.invoke(question)
                                
                                # Clean up the response
                                answer = output.split("Answer:")[1].strip() if "Answer:" in output else output.strip()
                                st.write("**Trả lời:**")
                                st.write(answer)
                                
                                add_message("assistant", answer)
                            except Exception as e:
                                st.error(f"Đã xảy ra lỗi: {e}")
                                add_message("assistant", f"Đã xảy ra lỗi: {e}")
        else:  
            st.info("Vui lòng xử lý PDF trước khi đặt câu hỏi.")  
            time.sleep(10)
            st.chat_input("Nhập câu hỏi của bạn...", disabled=True)
    else:
        st.info("Vui lòng đợi cho đến khi các mô hình được tải xong.")
        time.sleep(10)
        st.chat_input("Nhập câu hỏi của bạn...", disabled=True)
                             