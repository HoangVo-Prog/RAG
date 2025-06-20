#!/bin/bash

# Root folder
mkdir -p aio-rag
cd aio-rag || exit

# Tạo file chính
touch main.py
touch api.py
touch config.py
touch requirements.txt
touch .env
touch README.md

# Tạo thư mục và file app/core
mkdir -p app/core
touch app/core/__init__.py
touch app/core/embeddings.py
touch app/core/llm.py
touch app/core/pdf.py
touch app/core/rag_chain.py
touch app/core/prompt.py

# Tạo thư mục và file app/ui
mkdir -p app/ui
touch app/ui/__init__.py
touch app/ui/interface.py

# Tạo thư mục và file app/services
mkdir -p app/services
touch app/services/question_handler.py

# Tạo thư mục và file app/api
mkdir -p app/api
touch app/api/__init__.py
touch app/api/routes.py
touch app/api/schemas.py

# Tạo thư mục và file utils
mkdir -p utils
touch utils/logger.py
touch utils/file.py

echo "✅ Thư mục và file cấu trúc dự án đã được tạo xong tại thư mục ./aio-rag"
