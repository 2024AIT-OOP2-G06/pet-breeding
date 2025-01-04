from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from models import Pet

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

# ペット育成画面
@pet_bp.route('/care/<int:pet_id>', methods=['GET', 'POST'])
def care(pet_id):
    pet = Pet.get_or_none(Pet.type == pet_id)
    if not pet:
        return redirect(url_for('pet.list'))
 
    return render_template('pet_care.html')

