#!/usr/bin/env python3
import os
import shutil
import zipfile
import subprocess

def create_package():
    """Lambdaデプロイパッケージを作成"""
    # プロジェクトルートディレクトリを設定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # backend/lambda
    
    # 作業ディレクトリをプロジェクトルートに変更
    os.chdir(project_root)
    print(f"\n=== プロジェクトルート: {project_root} ===")
    
    # クリーンアップ
    if os.path.exists('lambda_function.zip'):
        os.remove('lambda_function.zip')

    print("\n=== パッケージングを開始します ===")
    
    try:
        # configファイルの存在確認と作成
        if not os.path.exists('config.py'):
            print("config.pyが見つかりません。../../backend/config.pyからコピーします。")
            shutil.copy2('../../backend/config.py', 'config.py')

        # 必要なファイルリスト
        required_files = [
            # エントリポイント
            'lambda_function.py',
            # devicesパッケージのコアファイル
            'devices/handlers/device_handlers.py',
            'devices/handlers/__init__.py',
            'devices/models.py',
            'devices/schemas.py',
            'devices/database.py',
            'devices/__init__.py',
            # 共通モジュール
            'devices/common/exceptions.py',
            'devices/common/__init__.py',
            # 設定ファイル
            'config.py',
            # 依存関係
            'requirements.txt'
        ]

        # 依存関係をインストール
        print("\n=== 依存関係をインストールしています ===")
        subprocess.check_call([
            'pip', 'install',
            '--target', '.',
            'fastapi==0.109.2',
            'mangum==0.19.0',
            'sqlalchemy==2.0.27',
            'mysql-connector-python==8.3.0',
            'pydantic==2.6.1',
            'python-dotenv==1.0.1',
            'typing_extensions',
            'starlette'
        ])

        # ZIPファイルを作成
        print("\n=== ZIPファイルを作成しています ===")
        with zipfile.ZipFile('lambda_function.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
            # 必要なファイルを追加
            for file_path in required_files:
                if os.path.exists(file_path):
                    # Windowsのパス区切り文字をUNIXスタイルに変換
                    arc_name = file_path.replace('\\', '/')
                    zf.write(file_path, arc_name)
                    print(f"✓ Added to ZIP: {arc_name}")
                else:
                    print(f"Warning: Required file not found: {file_path}")

            # インストールされた依存関係を追加
            for root, dirs, files in os.walk('.'):
                # .gitや__pycache__などを除外
                if any(part.startswith(('.', '__')) for part in root.split(os.sep)):
                    continue
                
                for file in files:
                    if file.endswith(('.py', '.so', '.pyd')):  # Pythonモジュールのみ
                        file_path = os.path.join(root, file)
                        # devicesディレクトリ以外の依存関係のみを追加
                        if not file_path.startswith('./devices/') and not file_path in required_files:
                            arc_name = os.path.relpath(file_path, '.').replace('\\', '/')
                            if not arc_name.startswith(('test_', 'setup.py')):  # テストファイルを除外
                                zf.write(file_path, arc_name)
                                print(f"✓ Added dependency: {arc_name}")

        # パッケージサイズを確認
        zip_size = os.path.getsize('lambda_function.zip') / (1024 * 1024)
        print(f"\nパッケージサイズ: {zip_size:.2f} MB")

        # ZIPファイルの構造を確認
        print("\n=== ZIPファイルの構造を確認 ===")
        with zipfile.ZipFile('lambda_function.zip', 'r') as zf:
            print("\nルートディレクトリの構造:")
            root_files = sorted(f for f in zf.namelist() if '/' not in f)
            for file in root_files:
                print(f"  - {file}")

            print("\ndevicesパッケージの構造:")
            devices_files = sorted(f for f in zf.namelist() if f.startswith('devices/'))
            for file in devices_files:
                print(f"  - {file}")

    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        raise
    finally:
        # 一時ファイルのクリーンアップ
        if os.path.exists('config.py') and os.path.exists('../../backend/config.py'):
            os.remove('config.py')
        print("\n✓ パッケージングが完了しました")

if __name__ == '__main__':
    create_package()