#!/bin/bash

# Function to detect if running in Jupyter or Colab
is_colab_or_notebook() {
  if [ -n "$COLAB_GPU" ] || [ -n "$JPY_PARENT_PID" ]; then
    return 0  # true
  else
    return 1  # false
  fi
}

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
  echo "📦 Installing pyngrok for public access..."
  pip install -q pyngrok
fi

# Install required libraries from requirements.txt
if [ -f "requirements.txt" ]; then
  echo "📦 Installing required Python libraries from requirements.txt..."
  pip install -q -r requirements.txt
else
  echo "❌ requirements.txt not found. Please make sure it exists in the project root."
  exit 1
fi

echo "✅ Environment setup complete."
