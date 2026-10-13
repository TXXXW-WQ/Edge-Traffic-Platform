FROM python:3.12-slim

# 1. 必要なシステムパッケージ（SUMOのビルド・実行、およびX11 GUI表示用ライブラリ）のインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# 2. uv のインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx

# 3. 作業ディレクトリの設定
WORKDIR /app

# 4. 依存関係定義ファイルのコピー
COPY pyproject.toml ./

# 5. 依存関係のインストール
RUN uv pip install --system --no-cache .

# 6. プロジェクトファイルをコピー
COPY . .