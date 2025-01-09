from peewee import Model, CharField, IntegerField
from .db import db

class Pet(Model):
    name = CharField()  # ペットの名前
    type = IntegerField()  # 種類(0:犬、1:猫、2:鳥)
    happiness = IntegerField(default=0)  # 幸福度
    level = IntegerField(default=1)  # ペットのレベル
    exp = IntegerField(default=0)  # 累積経験値（追加しました）

    class Meta:
        database = db
