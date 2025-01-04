from peewee import Model, CharField, IntegerField
from .db import db

class Pet(Model):
    name = CharField()  # ペットの名前
    type = IntegerField()  # 種類(0:犬、1:猫、2:鳥)
    # happiness = IntegerField()  # 幸福度
    # level = IntegerField()  # ペットのレベル

    class Meta:
        database = db
