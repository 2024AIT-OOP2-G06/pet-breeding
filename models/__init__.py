from peewee import SqliteDatabase
from .db import *
from .pet import Pet


# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    Pet,
    
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()