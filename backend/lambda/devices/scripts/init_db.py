from ..database import Base, engine
from ..models import Device

def init_database():
    print("データベーステーブルを作成します...")
    Base.metadata.drop_all(bind=engine)  # 既存のテーブルを削除
    Base.metadata.create_all(bind=engine)  # テーブルを再作成
    print("データベーステーブルの作成が完了しました。")

if __name__ == "__main__":
    init_database() 