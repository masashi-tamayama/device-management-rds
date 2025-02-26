#!/usr/bin/env python3
import os
import shutil
import subprocess
import zipfile
import glob

def create_package():
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    # 作業ディレクトリの作成とクリーンアップ
    package_dir = os.path.join(base_dir, "package")
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)

    print("\n=== パッケージングを開始します ===")
    
    # 必要なディレクトリ構造の作成
    os.makedirs(os.path.join(package_dir, "devices", "handlers"), exist_ok=True)
    
    # 必要なファイルをコピー
    required_files = [
        ("devices/handlers/device_handlers.py", "devices/handlers/device_handlers.py"),
        ("devices/models.py", "devices/models.py"),
        ("devices/schemas.py", "devices/schemas.py"),
        ("devices/database.py", "devices/database.py"),
        ("../../backend/config.py", "config.py")
    ]

    for src, dst in required_files:
        src_path = os.path.join(base_dir, src)
        dst_path = os.path.join(package_dir, dst)
        if os.path.exists(src_path):
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)

    # シンプルな__init__.pyファイルの作成
    with open(os.path.join(package_dir, "devices", "__init__.py"), "w") as f:
        f.write("")
    with open(os.path.join(package_dir, "devices", "handlers", "__init__.py"), "w") as f:
        f.write("")

    # 必要なライブラリをインストール
    lib_dir = os.path.join(package_dir, "lib")
    os.makedirs(lib_dir, exist_ok=True)
    
    requirements = [
        "fastapi==0.109.2",
        "mangum==0.19.0",
        "sqlalchemy==2.0.27",
        "mysql-connector-python==8.3.0",
        "pydantic==2.6.1",
        "typing_extensions",
        "starlette"
    ]
    
    for req in requirements:
        try:
            subprocess.run([
                "pip", "install",
                "--no-deps",
                req,
                "-t", lib_dir
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"警告: {req} のインストールに失敗しました: {e}")

    # ZIPファイルの作成
    zip_path = os.path.join(base_dir, "function.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)

    # 作業ディレクトリの削除
    shutil.rmtree(package_dir)
    
    print("\n=== パッケージングが完了しました ===")
    print(f"作成されたファイル: {zip_path}")

if __name__ == "__main__":
    create_package() 