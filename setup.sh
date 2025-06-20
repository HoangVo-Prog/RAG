#!/bin/bash

# Function to detect if running in Jupyter or Colab
is_colab_or_notebook() {
  if [ -n "$COLAB_GPU" ] || [ -n "$JPY_PARENT_PID" ]; then
    return 0  # true
  else
    return 1  # false
  fi
}

# Library versions
REQUIREMENTS=(
  "transformers==4.40.0"
  "langchain==0.1.20"
  "langchainhub==0.1.15"
  "langchain-chroma==0.1.8"
  "langchain_experimental==0.0.61"
  "langchain-community==0.0.38"
  "langchain_huggingface==0.0.3"
  "python-dotenv==1.0.0"
  "pypdf"
  "streamlit==1.36.0"
)

# If not running in Colab/Notebook, check for conda and create env
if ! is_colab_or_notebook; then
  if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
  fi

  echo "✅ Conda found. Creating conda environment..."
  conda create -y -n aio-rag python=3.11
  echo "✅ Activating conda environment..."
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate aio-rag
else
  echo "🔍 Running in Colab or Notebook environment. Skipping conda setup."
fi

# Install required libraries via pip
echo "📦 Installing required Python libraries..."
for pkg in "${REQUIREMENTS[@]}"; do
  pip install "$pkg"
done

echo "✅ Environment setup complete."
