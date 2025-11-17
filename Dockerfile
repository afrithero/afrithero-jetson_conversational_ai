FROM dustynv/l4t-pytorch:r36.4.0

ENV PIP_INDEX_URL=https://pypi.org/simple
ENV PIP_EXTRA_INDEX_URL=https://pypi.jetson-ai-lab.io/jp6/cu126/

WORKDIR /app

# ------------------------------
# System dependencies
# ------------------------------
RUN apt-get update && \
    apt-get install -y \
        wget \
        git \
        ffmpeg \
        libsndfile1 \
        alsa-utils \
        build-essential \
        cmake \
        libcurl4-openssl-dev \
        pkg-config \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*


# ------------------------------
# Build CTranslate2 GPU backend (JP6 best practice)
# ------------------------------
RUN git clone --recursive https://github.com/OpenNMT/CTranslate2.git && \
    cd CTranslate2 && \
    mkdir build && cd build && \
    cmake .. \
        -DWITH_CUDA=ON \
        -DWITH_CUDNN=ON \
        -DWITH_MKL=OFF \
        -DOPENMP_RUNTIME=COMP \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make -j$(nproc) && \
    make install && \
    ldconfig


# ------------------------------
# Build Faster-Whisper with GPU CTranslate2
# ------------------------------
RUN git clone https://github.com/SYSTRAN/faster-whisper.git && \
    cd faster-whisper && \
    CT2_DIR=/usr/local/lib/python3.10/dist-packages/ctranslate2 \
    pip install .


# ------------------------------
# Build llama.cpp (CUDA enabled)
# ------------------------------
RUN git clone https://github.com/ggml-org/llama.cpp && \
    cd llama.cpp && \
    cmake -B build \
        -DGGML_CUDA=ON \
        -DGGML_CUDA_F16=ON \
        -DLLAMA_CURL=ON \
        -DGGML_CUDA_FA_ALL_QUANTS=ON \
        -DCMAKE_CUDA_ARCHITECTURES="87" && \
    cmake --build build --config Release --parallel $(nproc)


# ------------------------------
# Install Python packages
# ------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ------------------------------
# Prepare model directories
# ------------------------------
RUN mkdir -p /app/models/gguf /app/models/whisper /app/models/piper


# ------------------------------
# Download Nemotron 8B GGUF and piper-tts model
# ------------------------------
RUN wget https://huggingface.co/bartowski/nvidia_Llama-3.1-Nemotron-Nano-8B-v1-GGUF/resolve/main/nvidia_Llama-3.1-Nemotron-Nano-8B-v1-Q4_K_M.gguf \
    -O /app/models/gguf/nemotron-8b-q4km.gguf

RUN wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx \ 
    -O /app/models/piper/voice.onnx

RUN wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json \ 
    -O /app/models/piper/voice.onnx.json

# ------------------------------
# Copy source code
# ------------------------------
COPY src/ .

# ------------------------------
# Start llama-server
# ------------------------------
CMD ["/app/llama.cpp/build/bin/llama-server", \
     "-m", "/app/models/gguf/nemotron-8b-q4km.gguf", \
     "--port", "8080", \
     "--gpu-layers", "999", \
     "--ctx-size", "4096"]
