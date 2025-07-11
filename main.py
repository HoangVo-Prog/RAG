import streamlit as st
import tempfile
import os
import torch
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_chroma import Chroma
from langchain_huggingface.llms import HuggingFacePipeline
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers import BitsAndBytesConfig
import time

# Session state initialization
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'models_loaded' not in st.session_state:
    st.session_state.models_loaded = False
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = None
if 'llm' not in st.session_state:
    st.session_state.llm = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = ""

# Functions
@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="bkai-foundation-models/vietnamese-bi-encoder")

@st.cache_resource  
def load_llm():
    MODEL_NAME = "lmsys/vicuna-7b-v1.5"

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_quant_type="nf4"
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        pad_token_id=tokenizer.eos_token_id,
        device_map="auto"
    )
    
    return HuggingFacePipeline(pipeline=model_pipeline)

def process_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
    
    loader = PyPDFLoader(tmp_file_path)
    documents = loader.load()
    
    semantic_splitter = SemanticChunker(
        embeddings=st.session_state.embeddings,
        buffer_size=1,
        breakpoint_threshold_type="percentile", 
        breakpoint_threshold_amount=95,
        min_chunk_size=500,
        add_start_index=True
    )
    
    docs = semantic_splitter.split_documents(documents)
    vector_db = Chroma.from_documents(documents=docs, embedding=st.session_state.embeddings)
    retriever = vector_db.as_retriever()
    
    prompt = hub.pull("rlm/rag-prompt")
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt 
        | st.session_state.llm
        | StrOutputParser()
    )
    
    os.unlink(tmp_file_path)
    return rag_chain, len(docs)

def add_message(role, content):
    """Thêm tin nhắn vào lịch sử chat"""
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "timestamp": time.time()
    })

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

# UI
def main():
    st.set_page_config(
        page_title="PDF RAG Chatbot", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("PDF RAG Assistant")
    st.logo("/kaggle/working/RAG/rag/app/image/logo.png", size="large")
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Cài đặt")
        
        # Load models
        if not st.session_state.models_loaded:
            st.warning("⏳ Đang tải models...")
            with st.spinner("Đang tải AI models..."):
                st.session_state.embeddings = load_embeddings()
                st.session_state.llm = load_llm()
                st.session_state.models_loaded = True
            st.success("✅ Models đã sẵn sàng!")
            st.rerun()
        else:
            st.success("✅ Models đã sẵn sàng!")

        st.markdown("---")
        
        # Upload PDF
        st.subheader("📄 Upload tài liệu")
        uploaded_file = st.file_uploader("Chọn file PDF", type="pdf")
        
        if uploaded_file:
            if st.button("🔄 Xử lý PDF", use_container_width=True):
                with st.spinner("Đang xử lý PDF..."):
                    st.session_state.rag_chain, num_chunks = process_pdf(uploaded_file)
                    st.session_state.pdf_processed = True
                    st.session_state.pdf_name = uploaded_file.name
                    # Reset chat history khi upload PDF mới
                    clear_chat()
                    add_message("assistant", f"✅ Đã xử lý thành công file **{uploaded_file.name}**!\n\n📊 Tài liệu được chia thành {num_chunks} phần. Bạn có thể bắt đầu đặt câu hỏi về nội dung tài liệu.")
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
            # User input
            user_input = st.chat_input("Nhập câu hỏi của bạn...")
            
            if user_input:
                # Add user message
                add_message("user", user_input)
                
                # Display user message immediately
                with st.chat_message("user"):
                    st.write(user_input)
                
                # Generate response
                with st.chat_message("assistant"):
                    with st.spinner("Đang suy nghĩ..."):
                        try:
                            output = st.session_state.rag_chain.invoke(user_input)
                            # Clean up the response
                            if 'Answer:' in output:
                                answer = output.split('Answer:')[1].strip()
                            else:
                                answer = output.strip()
                            
                            # Display response
                            st.write(answer)
                            
                            # Add assistant message to history
                            add_message("assistant", answer)
                            
                        except Exception as e:
                            error_msg = f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"
                            st.error(error_msg)
                            add_message("assistant", error_msg)
        else:
            st.info("🔄 Vui lòng upload và xử lý file PDF trước khi bắt đầu chat!")
            st.chat_input("Nhập câu hỏi của bạn...", disabled=True)
    else:
        st.info("⏳ Đang tải AI models, vui lòng đợi...")
        st.chat_input("Nhập câu hỏi của bạn...", disabled=True)

if __name__ == "__main__":
    main()
    