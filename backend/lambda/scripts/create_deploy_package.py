#!/usr/bin/env python3
import os
import pyminizip
import shutil
import subprocess

def create_deploy_package():
    # カレントディレクトリに移動
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)
    
    # 一時ディレクトリの作成
    temp_dir = os.path.join(base_dir, 'temp_package')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # 必要なアプリケーションファイル
    app_files = [
        ('devices/handlers/device_handlers.py', 'devices/handlers/device_handlers.py'),
        ('devices/models.py', 'devices/models.py'),
        ('devices/schemas.py', 'devices/schemas.py'),
        ('devices/database.py', 'devices/database.py'),
        ('../../backend/config.py', 'config.py')
    ]

    # __init__.pyファイルの作成
    os.makedirs(os.path.join(temp_dir, 'devices', 'handlers'), exist_ok=True)
    with open(os.path.join(temp_dir, 'devices', '__init__.py'), 'w') as f:
        pass

    # アプリケーションファイルのコピー
    for src, dst in app_files:
        src_path = os.path.join(base_dir, src)
        dst_path = os.path.join(temp_dir, dst)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)

    # 必要なライブラリをインストール
    print("必要なライブラリをインストールしています...")
    subprocess.run([
        "pip", "install",
        "--target", temp_dir,
        "fastapi==0.109.2",
        "mangum==0.19.0",
        "sqlalchemy==2.0.27",
        "mysql-connector-python==8.3.0",
        "pydantic==2.6.1",
        "typing_extensions",
        "starlette"
    ], check=True)

    # ライブラリファイルの収集
    files_to_include = []
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(('.py', '.so', '.pyd')):  # Windows用の.pydファイルも含める
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, temp_dir)
                files_to_include.append((full_path, rel_path))

    # ../function.zipを作成
    output_path = os.path.join(base_dir, '..', 'function.zip')
    
    # ZIPファイルを作成（圧縮レベル9で最大圧縮）
    pyminizip.compress_multiple(
        [f[0] for f in files_to_include],  # ソースファイルパス
        [f[1] for f in files_to_include],  # ZIPファイル内のパス
        output_path,                       # 出力ZIPファイル
        None,                             # パスワードなし
        9                                 # 最大圧縮レベル
    )
    
    # 一時ディレクトリの削除
    shutil.rmtree(temp_dir)
    
    print(f"\nデプロイパッケージを作成しました: {output_path}")
    print("\nパッケージの内容:")
    os.system(f"unzip -l {output_path}")

if __name__ == "__main__":
    create_deploy_package() 