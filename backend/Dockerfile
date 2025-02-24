FROM python:3.12-slim

WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    locales && \
    rm -rf /var/lib/apt/lists/* && \
    # 日本語ロケールの生成
    sed -i -E 's/# (ja_JP.UTF-8)/\1/' /etc/locale.gen && \
    locale-gen

# 環境変数の設定
ENV LANG=ja_JP.UTF-8 \
    LC_ALL=ja_JP.UTF-8 \
    TZ=Asia/Tokyo

# 依存関係のインストール
COPY ./lambda/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY ./lambda/ .

# 環境変数の設定
ENV PYTHONPATH=/app

# FastAPIアプリケーションの起動
CMD ["uvicorn", "devices.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 