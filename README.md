# device-management

# 🔧 機器管理システム

## 📌 プロジェクト概要
本プロジェクトは、AWS 環境で動作する **機器管理システム** です。  
機器の登録・編集・削除・一覧表示を行い、データは **RDS（MySQL）または DynamoDB** に保存されます。

## 📂 ディレクトリ構成
```
device-management/
│── backend/    # バックエンド（Lambda）
│   ├── lambda/ # AWS Lambda のコード置き場
│   │   ├── requirements.txt  # 依存ライブラリ（空のファイル）
│── frontend/   # フロントエンド（Reactなど）
│── README.md   # プロジェクトの説明
```

---

## 🏗️ 使用技術
### **フロントエンド**
- React（または Vue.js）
- AWS S3 + CloudFront

### **バックエンド**
- AWS Lambda（Python）
- API Gateway
- FastAPI
- MySQL（RDS）または DynamoDB

---

## 🚀 機能一覧
- 🔹 **機器一覧画面**
  - 登録された機器を一覧表示
- 🔹 **機器登録**
  - 新しい機器を登録
- 🔹 **機器編集**
  - 登録済み機器を更新
- 🔹 **機器削除**
  - 機器情報を削除

---

## 🔧 環境構築手順

### **1. GitHub リポジトリの作成**
開発を管理するために **GitHubリポジトリ** を作成します。

📌 **手順**
1. [GitHub](https://github.com/) にアクセスし、アカウントにログイン
2. **「New Repository（新しいリポジトリ）」** を作成
   - **リポジトリ名:** `device-management`
   - **Public（公開） or Private（非公開）:** 任意
   - **Readmeの追加:** 追加する
3. **作成したリポジトリのURLをコピー**

---

### **2. システム構成**
本システムは、AWS を活用して以下の構成で動作します。

---

#### **① フロントエンド（S3 + CloudFront）**
📌 **S3（Amazon Simple Storage Service）とは？**  
S3 は **静的なウェブサイトや画像、動画などのファイルを保存できるクラウドストレージ** です。  
React で作成したフロントエンドは、静的ファイル（HTML/CSS/JS）として出力されるため、S3 にアップロードすれば **サーバー不要で Web サイトを公開** できます。

📌 **CloudFront とは？**  
CloudFront は **CDN（コンテンツ配信ネットワーク）** の AWS サービスで、S3 に置いた静的ファイルを高速・安全に配信できます。

📌 **なぜ S3 + CloudFront を使うのか？**
- **S3** → フロントエンドの静的ファイルを保存
- **CloudFront** → ユーザーが素早くアクセスできるようにキャッシュ＆配信

💡 **React のプロジェクトを `npm run build` でビルドし、その出力フォルダを S3 にアップロードすれば、すぐに公開できます。**

---

#### **② バックエンド（API Gateway + Lambda）**
本システムのバックエンドは、AWS Lambda を使用してサーバーレスで動作します。

📌 **バックエンドの構成**
| 項目 | 説明 |
|----|----|
| **言語** | Python |
| **フレームワーク** | AWS Lambda（サーバーレスの実行環境） |
| **API** | API Gateway（フロントエンドと Lambda を繋ぐためのサービス） |

📌 **なぜ Lambda を使うのか？**
- **サーバー不要**（EC2 のようにサーバーを用意しなくてよい）
- **イベントドリブン**（API Gateway 経由でリクエストが来た時だけ処理を実行するのでコスト削減）
- **スケーラブル**（リクエスト数が増えても自動でスケール）

📌 **Lambda の基本的な動き**
1. **React（フロントエンド）から APIリクエスト**
2. **API Gateway がリクエストを受け取り、Lambda に転送**
3. **Lambda が Python コードを実行 し、データベース（RDS/DynamoDB）とやり取り**
4. **処理結果を API Gateway 経由でフロントエンドに返す**

---

#### **③ データベース（RDS vs DynamoDB）**
本システムでは、データの保存方法として **RDS（MySQL）** または **DynamoDB** を利用できます。

📌 **データベースの選択**
| パターン | データベース | 保存形式 |
|----|----|----|
| **パターン1** | RDS（MySQL） | JSON として受け取るが、内部ではリレーショナル形式（テーブル） |
| **パターン2** | DynamoDB | JSON 形式のまま保存（NoSQL） |

📌 **RDS（MySQL）のデータ保存方法**
RDS は **リレーショナルデータベース** なので、データは **テーブル形式** で保存されます。

```sql
CREATE TABLE devices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL
);
```
📌 **DynamoDB のデータ保存方法**
DynamoDB は **NoSQLデータベース** なので、データはそのまま JSON 形式で保存されます。

```json
{
    "id": "device123",
    "name": "エアコン",
    "manufacturer": "Panasonic"
}
```

📌 **どちらも JSON 形式で保存する？**
- **MySQL（RDS）** → JSON 形式で受け取るが、内部ではテーブルに変換  
- **DynamoDB** → そのまま JSON 形式で保存

💡 **つまり、フロントエンドから送るデータは JSON 形式ですが、RDS と DynamoDB では保存の仕方が違います。**

---

### **④ まとめ**
| 項目 | 説明 |
|----|----|
| **フロントエンド** | React を使用し、S3 に静的ファイルを配置し、CloudFront で配信 |
| **バックエンド** | AWS Lambda（Python）を API Gateway 経由で呼び出す |
| **データベース** | RDS（MySQL）はリレーショナルデータとして保存、DynamoDB は JSON のまま保存 |


# Python 環境構築（Windows 11）

## 1️⃣ Python のインストール手順（Windows 11）

### ✅ 正しい Python のダウンロード
1. [Python 公式サイト](https://www.python.org/downloads/windows/) にアクセス
2. 「Looking for a specific release?」のセクションから最新の安定版を選択
3. **「Windows installer (64-bit)」** をダウンロード  
   ✅ `python-3.x.x-amd64.exe` を選ぶ（Microsoft Store 版ではない）

### ✅ インストール手順
1. **ダウンロードしたインストーラーを実行**
2. **「Add Python to PATH」にチェックを入れる**
3. **「Install Now」をクリック**
4. **インストール完了後、「Disable path length limit」をクリック**
5. **PC を再起動**

---

## 2️⃣ インストール後の確認と Microsoft Store の影響チェック

### ✅ Python の動作確認
```bash
python --version
python3 --version
pip --version

**成功表示**
Python 3.13.2
Python 3.13.2
pip 24.3.1 from C:\Program Files\Python313\Lib\site-packages\pip (python 3.13)
```

# ✅ AWS CLI のインストール & 設定 (#7/2.3)

## 📝 概要
この手順では、Windows 11 環境で **AWS CLI** を **Microsoft Store 版の影響を受けずに** 正しくインストールし、GitBash で使用できるように設定します。

---

## 📌 **1. AWS CLI のインストール**
### ✅ **AWS CLI を公式サイトからダウンロード & インストール**
1. [AWS CLI 公式ダウンロードページ](https://awscli.amazonaws.com/AWSCLIV2.msi) にアクセス
2. `AWSCLIV2.msi`（Windows 64-bit 版）をダウンロード
3. ダウンロードした `AWSCLIV2.msi` を実行
4. **「Add AWS CLI to PATH」にチェックが入っていることを確認**
5. **「Install」をクリック**
6. インストール完了後、PC を再起動

---

## 📌 **2. AWS CLI の動作確認**
### ✅ **AWS CLI のバージョン確認**
```bash
aws --version
```
**期待する出力**
```
aws-cli/2.x.x Python/3.x.x Windows/11 exe/AMD64
```

---

## 📌 **3. AWS CLI の初期設定**
### ✅ **IAM ユーザーの作成**
1. **AWS マネジメントコンソールにログイン**
2. **[IAM ユーザー作成ページ](https://console.aws.amazon.com/iamv2/home?#/users) にアクセス**
3. **ユーザー名を入力**（例: `okita-cli-user`）
4. **「AWS マネジメントコンソールへのアクセス」を無効化**
5. **「アクセスキーを作成」**
6. **「コマンドラインインターフェイス (CLI)」にチェックを入れる**
7. **適切な説明タグを設定**（例: `AWS CLI access key for local development`）
8. **「作成」**

### ✅ **AWS CLI に認証情報を設定**
IAM ユーザーの **アクセスキー ID & シークレットキー** を取得し、以下のコマンドを実行：

```bash
aws configure
```

**入力内容**
```
AWS Access Key ID [None]: AKIA***************
AWS Secret Access Key [None]: *********************
Default region name [None]: ap-northeast-1
Default output format [None]: json
```

### ✅ **AWS CLI の認証情報確認**
```bash
aws configure list
```

---

## 📌 **4. AWS CLI の動作確認**
### ✅ **現在の AWS アカウント情報を取得**
```bash
aws sts get-caller-identity
```
**期待する出力**
```json
{
    "UserId": "AIDA42PHHUNFXVAGTNQAE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/okita-test"
}
```

### ✅ **S3 バケットの一覧を取得**
```bash
aws s3 ls
```
**バケットが存在しない場合、何も表示されなくても OK！**

### ✅ **EC2 インスタンスの一覧を取得**
```bash
aws ec2 describe-instances
```
**まだ EC2 を作成していなければ `Reservations: []` のように空のリストが表示される。**

---

## ✅ **セットアップ完了！**
✅ **AWS CLI を公式サイトからインストール**  
✅ **環境変数を設定し、AWS CLI が GitBash で使用できることを確認**  
✅ **`aws configure` で IAM ユーザーの認証情報を設定**  
✅ **AWS CLI から AWS に接続 & 操作できることを確認**  

🚀 **これで AWS CLI のセットアップが完了しました！** 🎉

---

# ✅ Node.js（React 用）のインストール (#8/2.4)

## 📝 概要
この手順では、Windows 11 環境に **React 開発用の Node.js** を正しくインストールし、動作確認を行います。

---

## 📌 **1. Node.js のインストール**
### ✅ **公式サイトからダウンロード & インストール**
1. [Node.js 公式ダウンロードページ](https://nodejs.org/ja/download/) にアクセス
2. **「LTS（推奨版）」の Windows 版（64-bit）** を選択し、ダウンロード
3. ダウンロードした `node-vxx.x.x-x64.msi` を実行
4. **「Next」→「I accept the terms」→「Next」**
5. **「Add to PATH」にチェックが入っていることを確認**
6. **「Install」をクリック**
7. インストール完了後、PC を再起動

---

## 📌 **2. Node.js の動作確認**
### ✅ **Node.js & npm のバージョン確認**
```bash
node -v
npm -v
```
**期待する出力（例）**
```
v18.16.1  # Node.js のバージョン（LTS）
9.5.1     # npm のバージョン
```
✅ **`node` と `npm` のバージョンが表示されれば成功！**

---

## 📌 **3. 環境変数の確認**
### ✅ **GitBash で確認**
```bash
echo $PATH | tr ':' '\n' | grep node
```
✅ **`C:\Program Files\nodejs` が含まれていれば OK！**

### ✅ **PowerShell で確認**
```powershell
$env:Path -split ";"
```
✅ **`C:\Program Files\nodejs` がリストにあれば OK！**

---

## 📌 **4. `npx` の動作確認**
React プロジェクトを作成する際に使用する `npx` が動作するか確認。

```bash
npx --version
```
✅ **エラーなくバージョンが表示されれば OK！**

---

## 📌 **5. React プロジェクトの作成テスト**
**React のセットアップが正しくできるか確認するため、一時的なテストプロジェクトを作成。**

```bash
npx create-react-app test-app
```

**正常にプロジェクトが作成できたら削除**
```bash
rm -rf test-app
```
✅ **`npx create-react-app` がエラーなく動作すれば成功！**

---

## ✅ **セットアップ完了！**
✅ **Node.js を公式サイトからインストール**  
✅ **環境変数を設定し、GitBash で `node` & `npm` が動作することを確認**  
✅ **`npx create-react-app` が正常に動作することを確認**  
✅ **開発環境に影響しないクリーンなセットアップを実施**  

---

# ✅ React 環境のセットアップ (#10/2.6)

## 📝 概要
この手順では、**Vite + React（TypeScript + SWC）を使用して、最新の React 開発環境をセットアップ** します。

---

## 📌 **1. React プロジェクトの作成**
### ✅ **Vite を使って React 環境をセットアップ**
```bash
npm create vite@latest frontend --template react
```
✅ **対話形式で以下のオプションを選択**
- `Select a framework:` **React**
- `Select a variant:` **TypeScript + SWC**

---

## 📌 **2. 依存関係のインストール**
### ✅ `frontend/` ディレクトリに移動して `npm install` を実行
```bash
cd frontend
npm install
```
✅ **エラーが出なければ成功！**

---

## 📌 **3. React アプリの起動**
```bash
npm run dev
```
✅ **ターミナルに以下のようなメッセージが表示される**
```
  VITE v6.1.0  ready in 477 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```
✅ **ブラウザで `http://localhost:5173/` にアクセスし、React アプリが動作していることを確認！**

---

## 📌 **4. React 開発サーバーの停止方法**
### ✅ `Ctrl + C` を押して開発サーバーを停止
```bash
Ctrl + C
```
✅ **`Terminate batch job (Y/N)?` のようなメッセージが出た場合、`Y` を入力して Enter**

**もし `Ctrl + C` が効かない場合は、以下の方法で強制終了**
```bash
lsof -i :5173  # Vite のプロセス ID（PID）を確認
kill -9 <PID>  # プロセスを強制終了
```

---

## 📌 **5. よくあるエラーと解決策**
### **❌ `npm install` 実行時に `package.json` が見つからないエラー**
```
npm error enoent Could not read package.json: Error: ENOENT: no such file or directory
```
✅ **解決策**
```bash
npm create vite@latest . --template react
npm install
```
🔹 `package.json` がない場合、上記のコマンドで `frontend/` に Vite のプロジェクトを作成し直す。

---

### **❌ `npm create vite@latest . --template react` 実行時に `Current directory is not empty.`**
```
? Current directory is not empty. Please choose how to proceed: 
  > Remove existing files and continue
    Ignore files and continue
    Cancel operation
```
✅ **解決策**
- **既存の `frontend/` をリセットするなら `Remove existing files and continue`**
- **既存のファイルを保持したいなら `Ignore files and continue`**
- **一旦キャンセルして確認するなら `Cancel operation`**

---

## ✅ **セットアップ完了！**
✅ **最新の方法（Vite）で React 環境をセットアップ**  
✅ **`npm install` で依存関係をインストール**  
✅ **`npm run dev` でローカル開発環境を起動できることを確認**  
✅ **開発サーバーの停止方法も記載**  

---

# ✅ 環境変数の管理（.env の作成） (#11/2.7)

## 📝 概要
この手順では、**バックエンド（Python）とフロントエンド（React）で `.env` を使って環境変数を管理する方法** を説明します。

---

## 📌 **1. `.env` ファイルの作成**
### ✅ **バックエンド（Python）**
```bash
cd backend
touch .env
```
**`backend/.env` に記述する環境変数**
```
DATABASE_URL=mysql://user:password@localhost:3306/mydatabase
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
SECRET_KEY=your-secret-key
```

### ✅ **フロントエンド（React / Vite）**
```bash
cd frontend
touch .env
```
**`frontend/.env` に記述する環境変数**
```
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=ReactApp
```
⚠ **Vite の環境変数は `VITE_` で始める必要がある** ので注意。

---

## 📌 **2. `.env` を Git 管理対象外にする**
```bash
echo ".env" >> backend/.gitignore
echo ".env" >> frontend/.gitignore
```
✅ **これで `.env` は Git にコミットされなくなり、安全に管理できる！**

---

## 📌 **3. Python 側で `.env` を読み込む**
### ✅ **`python-dotenv` をインストール**
```bash
pip install python-dotenv
```

### ✅ **`backend/config.py` に `.env` を読み込むコードを追加**
```python
import os
from dotenv import load_dotenv

# .env を読み込む
load_dotenv()

# 環境変数の取得
DATABASE_URL = os.getenv("DATABASE_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# 環境変数の確認（デバッグ用）
print(f"Database URL: {DATABASE_URL}")
```

### ✅ **環境変数の読み込みを確認**
```bash
python config.py
```
✅ **エラーがなく、環境変数が正しく表示されれば成功！**

---

## 📌 **4. React（Vite）側で `.env` を読み込む**
### ✅ **`frontend/src/config.ts` を作成**
```typescript
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
export const APP_NAME = import.meta.env.VITE_APP_NAME;
```

### ✅ **`frontend/src/App.tsx` で環境変数を表示**
```tsx
import { API_BASE_URL, APP_NAME } from "./config";

function App() {
  return (
    <div>
      <h1>{APP_NAME}</h1>
      <p>API Base URL: {API_BASE_URL}</p>
    </div>
  );
}

export default App;
```

### ✅ **環境変数の読み込みを確認**
```bash
npm run dev
```
**期待する出力**
```
  VITE v6.1.0  ready in 400 ms

  ➜  Local:   http://localhost:5173/
```
✅ **ブラウザで `http://localhost:5173/` にアクセスし、環境変数が表示されれば成功！**

---

## 🚀 S3 バケット設定手順 (フロントエンド用)

### 1️⃣ S3 バケットの作成
以下のコマンドで、フロントエンドのアセットをホスティングするための S3 バケットを作成します。

```bash
aws s3api create-bucket --bucket device-mgmt-frontend-bucket --region ap-northeast-1 --create-bucket-configuration LocationConstraint=ap-northeast-1
```

✅ **成功時の出力例**
```json
{
    "Location": "http://device-mgmt-frontend-bucket.s3.amazonaws.com/"
}
```

---

### 2️⃣ S3 バケットの公開設定
デフォルトではバケットが非公開になっているため、以下のコマンドで公開アクセスを許可します。

```bash
aws s3api put-public-access-block --bucket device-mgmt-frontend-bucket --public-access-block-configuration '{"BlockPublicAcls":false,"BlockPublicPolicy":false,"IgnorePublicAcls":false,"RestrictPublicBuckets":false}'
```

✅ **設定確認**
```bash
aws s3api get-public-access-block --bucket device-mgmt-frontend-bucket
```
🔹 **期待される出力**
```json
{
    "PublicAccessBlockConfiguration": {
        "BlockPublicAcls": false,
        "IgnorePublicAcls": false,
        "BlockPublicPolicy": false,
        "RestrictPublicBuckets": false
    }
}
```

---

### 3️⃣ バケットの作成を確認
作成したバケットが正しく登録されているかを確認するには、以下のコマンドを実行します。

```bash
aws s3api list-buckets
```

✅ **期待される出力**
```json
{
    "Buckets": [
        {
            "Name": "device-mgmt-frontend-bucket",
            "CreationDate": "2025-02-18T10:40:24+00:00"
        }
    ]
}
```

---

### ✅ 設定完了 🎉
これで、フロントエンドの静的ファイルを S3 にアップロードし、ホスティングする準備が整いました！ 🚀


---

# 🚀 CloudFront を使用した S3 静的サイトホスティング

## **1️⃣ CloudFront S3 Access Denied エラーの発生と解消手順**

### **❌ エラー発生のタイミング**
CloudFront を通じて S3 にホストした静的サイト (`index.html`) にアクセスした際に、**以下のエラーが発生しました。**

```xml
<Error>
<Code>AccessDenied</Code>
<Message>Access Denied</Message>
<RequestId>Q8ZNTG61DHYVZY2R</RequestId>
<HostId>fquG2agx//MMoGK8iN/96xH2RyBM1ITVwjwaAfH68pZpV1GaigsRs2Gtyyo8ByHPwkahB+rMmGaOnHyP5kvQV7Y5ezcIiSzJqwKwocf30cs=</HostId>
</Error>
```

**このエラーの原因**
1. **CloudFront のオリジン設定が誤っていた**
   - `distribution-config.json` の `"Origins.DomainName"` が `d1zw3p63uw42m7.cloudfront.net` になっており、本来指定すべき `device-mgmt-frontend-bucket.s3.amazonaws.com` になっていなかった。

2. **S3 バケットが CloudFront からのアクセスを許可していなかった**
   - S3 バケットポリシーが CloudFront からの `s3:GetObject` を許可していなかった。

3. **S3 のパブリックアクセス設定が適切でなかった**
   - `"BlockPublicPolicy": true` になっており、CloudFront 経由のリクエストもブロックされていた。

4. **CloudFront のキャッシュが古い設定を保持していた**
   - 設定を変更しても、CloudFront に古いバージョンがキャッシュされており、更新が適用されていなかった。

---

## **2️⃣ CloudFront S3 Access Denied エラーの解決手順**

### **1. Origin Access Control (OAC) の作成**
```bash
aws cloudfront create-origin-access-control \
    --origin-access-control-config '{
        "Name": "device-mgmt-frontend-OAC",
        "Description": "OAC for frontend",
        "SigningBehavior": "always",
        "SigningProtocol": "sigv4",
        "OriginAccessControlOriginType": "s3"
    }'
```

✅ **作成された OAC の ID (`E1JCQCLG0RPNWU`) を取得し、CloudFront に適用。**

---

### **2. CloudFront のオリジン設定を OAC に更新**
#### **📌 `distribution-config.json` 修正**
```json
"Origins": {
    "Items": [
        {
            "Id": "device-mgmt-frontend-bucket",
            "DomainName": "device-mgmt-frontend-bucket.s3.amazonaws.com",
            "OriginAccessControlId": "E1JCQCLG0RPNWU"
        }
    ]
}
```

✅ **CloudFront の設定を適用**
```bash
aws cloudfront update-distribution --id E1OJBU6FBKY6X --if-match $(aws cloudfront get-distribution --id E1OJBU6FBKY6X --query "ETag" --output text) --distribution-config file://distribution-config.json
```

---

### **3. S3 バケットポリシーを更新**
#### **📌 `bucket-policy.json`**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::device-mgmt-frontend-bucket/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::881490109259:distribution/E1OJBU6FBKY6X"
                }
            }
        }
    ]
}
```

✅ **バケットポリシーを適用**
```bash
aws s3api put-bucket-policy --bucket device-mgmt-frontend-bucket --policy file://bucket-policy.json
```

---

### **4. S3 のパブリックアクセス設定を修正**
```bash
aws s3api put-public-access-block \
    --bucket device-mgmt-frontend-bucket \
    --public-access-block-configuration '{
        "BlockPublicAcls": true,
        "IgnorePublicAcls": true,
        "BlockPublicPolicy": false,
        "RestrictPublicBuckets": false
    }'
```

---

### **5. テストファイルのアップロードとキャッシュ無効化**
CloudFront の設定変更が正しく適用されているかを確認するため、**テスト用の `index.html` をアップロード** し、**キャッシュを無効化** しました。

```bash
# テスト用 HTML ファイルを作成
echo "<html><body><h1>Hello from S3 via CloudFront</h1></body></html>" > index.html

# S3 にアップロード
aws s3 cp index.html s3://device-mgmt-frontend-bucket/

# CloudFront のキャッシュを無効化
aws cloudfront create-invalidation --distribution-id E1OJBU6FBKY6X --paths "/*"
```

✅ **S3 にファイルをアップロードし、キャッシュをクリアすることで最新の変更が反映される**

---

### **6. 動作確認**
```bash
https://d1zw3p63uw42m7.cloudfront.net/index.html
```
✅ **"Hello from S3 via CloudFront" が表示されれば成功 🎉**

---

## **3️⃣ 重要なポイント**
1. **OAC の作成と正しい ID の設定**
2. **CloudFront 設定での OAC ID の正確な反映**
3. **S3 バケットポリシーでの CloudFront サービスプリンシパルの許可**
4. **パブリックアクセスブロック設定の適切な構成**
5. **キャッシュ無効化による変更の反映**
6. **テスト用ファイルのアップロードと CloudFront 経由でのアクセス確認**

---

## **4️⃣ まとめ**
この手順により、S3 を **パブリックにせず、CloudFront 経由でのみアクセスできる構成** が完成しました。

---

# 🔧 機器管理システム

[... existing content ...]

# ✅ MySQL環境構築（Windows 11）

## 📝 概要
この手順では、Windows 11環境でMySQLをセットアップし、アプリケーションから接続できる状態にするまでの手順を説明します。

## 📌 1. MySQLのインストール
### ✅ MySQL Installerのダウンロード & インストール
1. [MySQL公式サイト](https://dev.mysql.com/downloads/installer/)からMySQL Installerをダウンロード
2. インストーラーを実行し、以下の項目を選択：
   - MySQL Server 8.0
   - MySQL Workbench
   - MySQL Shell
   - Connector/Python

### ✅ サーバー設定
1. **Windows Service設定**
   - Configure MySQL Server as a Windows Service: ✓
   - Service Name: MySQL80
   - Start the MySQL Server at System Startup: ✓
   - Standard System Account: ✓

2. **認証設定**
   - Authentication Method: Use Strong Password Encryption
   - Root Password: 設定したパスワードを安全に保管

## 📌 2. データベースとテーブルの作成
### ✅ MySQL Workbenchでの接続設定
1. MySQL Workbenchを起動
2. 「+」ボタンで新規接続を作成：
   - Connection Name: Local MySQL80
   - Hostname: localhost
   - Port: 3306
   - Username: root
   - Password: 設定したパスワード
   - Default Schema: lambdadb

### ✅ データベースとテーブルの作成
```sql
-- データベース作成
CREATE DATABASE lambdadb;
USE lambdadb;

-- デバイステーブルの作成
CREATE TABLE devices (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT '機器名',
    manufacturer VARCHAR(255) NOT NULL COMMENT 'メーカー名',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックスの作成
CREATE INDEX idx_devices_name ON devices(name);
CREATE INDEX idx_devices_manufacturer ON devices(manufacturer);

-- テーブルコメントの設定
ALTER TABLE devices COMMENT = '機器管理用のテーブル';
```

## 📌 3. アプリケーション設定
### ✅ 環境変数の設定
`backend/.env`ファイルに以下の設定を追加：
```
# データベース設定
DB_TYPE=rds

# RDS設定
RDS_HOST=localhost
RDS_PORT=3306
RDS_USER=root
RDS_PASSWORD=your_password
RDS_DATABASE=lambdadb
```

### ✅ 動作確認
1. テストデータの挿入：
```sql
INSERT INTO devices (id, name, manufacturer) VALUES 
(UUID(), 'エアコン', 'パナソニック'),
(UUID(), '冷蔵庫', '日立'),
(UUID(), '洗濯機', 'シャープ');
```

2. Pythonスクリプトでの接続テスト：
```bash
cd backend/lambda
python devices/scripts/insert_test_data.py
```

## 📌 4. トラブルシューティング
### ✅ よくあるエラーと解決策
1. **Access denied for user 'root'@'localhost'**
   - MySQLのrootパスワードが正しく設定されているか確認
   - `.env`ファイルのパスワードが正しいか確認

2. **Can't connect to MySQL server on 'localhost'**
   - MySQL Serverが起動しているか確認
   - ポート3306が使用可能か確認

3. **MySQL server has gone away**
   - データベース接続のタイムアウト設定を確認
   - データベースの負荷やネットワークの状態を確認

---

# 🚀 Swagger UI / ReDoc 使用ガイド

## 📝 概要
このガイドでは、FastAPIが提供する2つのAPIドキュメントツール（Swagger UIとReDoc）の使用方法について説明します。

## 🛠️ 前提条件

### 必要なパッケージ
```bash
pip install fastapi uvicorn
```

## 🔧 開発サーバーの起動手順

### 1. PowerShellを開く
スタートメニューまたは `Win + X` から PowerShellを起動します。

### 2. プロジェクトディレクトリに移動
```powershell
cd C:\Users\your-username\projects\device-management\backend\lambda
```

### 3. PYTHONPATHの設定とサーバー起動
```powershell
$env:PYTHONPATH = "." ; python -m uvicorn devices.main:app --reload
```

### 4. 起動確認
以下のようなメッセージが表示されれば成功です：
```
INFO:     Will watch for changes in these directories: ['C:\\Users\\...']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using StatReload
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 📚 APIドキュメントへのアクセス

### Swagger UI
- URL: http://127.0.0.1:8000/docs
- 特徴：
  - インタラクティブなAPIテスト機能
  - リクエスト/レスポンスの例を表示
  - 実際のAPIを試すことが可能

### ReDoc
- URL: http://127.0.0.1:8000/redoc
- 特徴：
  - 読みやすいドキュメント形式
  - 詳細なスキーマ情報
  - 印刷に適したレイアウト

## 💡 Swagger UIの使用方法

### 1. エンドポイントの選択
- 画面左側のエンドポイント一覧から操作したいAPIを選択
- 例：`PUT /api/v1/devices/{device_id}`

### 2. APIのテスト
1. 「Try it out」ボタンをクリック
2. パラメータを入力
   - URLパラメータ（例：`device_id`）
   - リクエストボディ（必要な場合）
3. 「Execute」ボタンをクリック
4. レスポンスを確認

### リクエスト例（デバイス更新）
```json
{
  "name": "更新後のデバイス名",
  "manufacturer": "更新後のメーカー名"
}
```

### レスポンス例
```json
{
  "name": "更新後のデバイス名",
  "manufacturer": "更新後のメーカー名",
  "id": "device-id",
  "created_at": "2024-02-20T10:00:00",
  "updated_at": "2024-02-20T11:00:00"
}
```

## 📖 ReDocの使用方法

### 1. スキーマの確認
- 左側のメニューから確認したいエンドポイントを選択
- リクエスト/レスポンスのスキーマ情報を確認

### 2. モデルの確認
- 画面右側に表示されるモデル定義を確認
- 各フィールドの型や制約を確認

## ⚠️ 注意事項

### セキュリティ
- 開発環境でのみ使用してください
- 本番環境では無効化することを推奨

### サーバーの停止方法
1. PowerShellウィンドウで `Ctrl + C` を押す
2. サーバープロセスが終了することを確認

## 🔍 トラブルシューティング

### サーバーが起動しない場合
1. ポート8000が使用中でないか確認
2. 必要なパッケージがインストールされているか確認
3. PYTHONPATHが正しく設定されているか確認

### ドキュメントにアクセスできない場合
1. サーバーが正常に起動しているか確認
2. URLが正しいか確認（http://127.0.0.1:8000/docs または /redoc）
3. ファイアウォールの設定を確認

## 📝 補足情報

### カスタマイズ可能な項目
- タイトル
- 説明
- バージョン
- タグ
- セキュリティ定義

### ドキュメント生成の自動化
- APIのコードからドキュメントが自動生成
- コードの変更が即座にドキュメントに反映
- OpenAPI（Swagger）仕様に準拠

---

# 🚀 Swagger UI / ReDoc 使用ガイド

## 📝 概要
このガイドでは、FastAPIが提供する2つのAPIドキュメントツール（Swagger UIとReDoc）の使用方法について説明します。

---

## 🛠️ 前提条件

### 必要なパッケージのインストール（初回のみ）
```bash
pip install fastapi uvicorn
```
※ パッケージのインストールは初回のみ必要です。一度インストールすれば、以降は再インストール不要です。

### インストール状態の確認方法
```bash
pip list | findstr "fastapi"
pip list | findstr "uvicorn"
```

## 🔧 開発サーバーの起動手順

### 1. PowerShellを開く
スタートメニューまたは `Win + X` から PowerShellを起動します。

### 2. プロジェクトディレクトリに移動
```powershell
cd C:\Users\your-username\projects\device-management\backend\lambda
```

### 3. PYTHONPATHの設定とサーバー起動
```powershell
$env:PYTHONPATH = "." ; python -m uvicorn devices.main:app --reload
```
※ `python -m`を使用することで、インストール済みのuvicornを確実に実行できます。

// ... 既存の内容は変更なし ...

---