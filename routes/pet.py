from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models import Pet
import time
import threading

# Blueprintの作成
pet_bp = Blueprint('pet', __name__, url_prefix='/')

# トップページ
@pet_bp.route('/', methods=['GET'])
def index():
    pets = Pet.select()

    return render_template('index.html', pets=pets)

# ペット作成画面
@pet_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']

        Pet.create(name=name, type=type)
        return redirect(url_for('pet.list'))
    
    return render_template('pet_add.html')

# ペット一覧画面
@pet_bp.route('/list')
def list():
    pets = Pet.select()
    return render_template('pet_list.html', items=pets)

# 幸福度を減少させる関数（10秒ごとに実行）
def decrease_happiness_periodically():
    while True:
        time.sleep(10)  # 10秒待機
        pets = Pet.select()  # 全てのペットを取得
        for pet in pets:
            if pet.happiness > 0:
                pet.happiness -= 1  # 幸福度を1減少
                pet.save()  # 更新を保存

# 別スレッドで定期的に幸福度を減少させる処理を実行
threading.Thread(target=decrease_happiness_periodically, daemon=True).start()


# ペット育成画面
@pet_bp.route('/care/<int:pet_id>', methods=['GET', 'POST'])
def care(pet_id):
    pet = Pet.get_or_none(Pet.id == pet_id)
    if not pet:
        return redirect(url_for('pet.list'))
    
    if request.method == 'POST':
        # アクションに応じて幸福度を増加
        action = request.form['action']
        happiness_increase = 0

        if action == 'feed':  # 餌をあげる
            happiness_increase = 20
        elif action == 'play':  # 遊ぶ
            happiness_increase = 20
        elif action == 'clean':  # 掃除する
            happiness_increase = 30
        elif action == 'reset':
            pet.happiness = 0
            pet.save()
            return redirect(url_for('pet.care', pet_id=pet_id))

        # 幸福度が 100 未満の場合にのみ増加
        if pet.happiness < 100:
            remaining_happiness = 100 - pet.happiness
            actual_increase = min(happiness_increase, remaining_happiness)  # 実際に増加する幸福度
            pet.happiness += actual_increase  # 幸福度の増加
            pet.exp += actual_increase  # 増加した分を経験値に加算

            # レベルアップ計算
            level_up_threshold = 70
            level_ups = pet.exp // level_up_threshold  # 経験値が70の倍数ごとにレベルアップ
            if level_ups > 0:
                # レベルが最大値（10）に達していない場合のみレベルアップ
                if pet.level < 10:
                    pet.level += level_ups
                    # レベルが10を超えないように調整
                    if pet.level > 10:
                        pet.level = 10
                        
                pet.exp %= level_up_threshold  # 余剰経験値を保存

        # ペットのレベルが10に達した場合、自動的に削除
        #if pet.level >= 10:
         #   pet.delete_instance()
          #  flash('ペットがレベル10に達したため削除されました。', 'info')
           # return redirect(url_for('pet.list'))

        # データベースに保存
        pet.save()

        return redirect(url_for('pet.care', pet_id=pet_id))
 
    return render_template('pet_care.html', pet=pet)

# 幸福度の状態を返すAPI
@pet_bp.route('/state/<int:pet_id>', methods=['GET'])
def get_state(pet_id):
    pet = Pet.get_or_none(Pet.id == pet_id)
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404
    
    return jsonify({
        'happiness': pet.happiness,
        'level': pet.level,
        'exp': pet.exp
    })