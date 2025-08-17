from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import db, Car
from forms import CarForm
import config

app = Flask(__name__)

# --- Config ---
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# DB'yi ilk çalıştırmada oluştur
with app.app_context():
    db.create_all()

# --------------------
# HTML Rotaları (mevcut akışın aynısı)
# --------------------
@app.route('/')
def index():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)

@app.route('/add', methods=['GET', 'POST'])
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(name=form.name.data, year=form.year.data, mileage=form.mileage.data)
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_car.html', form=form)

@app.route('/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = CarForm(obj=car)
    if form.validate_on_submit():
        car.name = form.name.data
        car.year = form.year.data
        car.mileage = form.mileage.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_car.html', form=form)

@app.route('/delete/<int:car_id>')
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('index'))

# --------------------
# JSON API (Postman / otomasyon testleri için)
# --------------------
def car_to_dict(c: Car) -> dict:
    return {"id": c.id, "name": c.name, "year": c.year, "mileage": c.mileage}

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({"status": "ok"}), 200

# Listele
@app.route('/api/cars', methods=['GET'])
def api_list_cars():
    cars = Car.query.order_by(Car.id.desc()).all()
    return jsonify([car_to_dict(c) for c in cars]), 200

# Oluştur
@app.route('/api/cars', methods=['POST'])
def api_create_car():
    data = request.get_json(silent=True) or {}
    required = ['name', 'year', 'mileage']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Gerekli alan(lar) eksik: {', '.join(missing)}"}), 400
    try:
        car = Car(
            name=str(data['name']),
            year=int(data['year']),
            mileage=int(data['mileage'])
        )
    except (ValueError, TypeError):
        return jsonify({"error": "year ve mileage sayı olmalı"}), 400

    db.session.add(car)
    db.session.commit()
    return jsonify(car_to_dict(car)), 201

# Detay
@app.route('/api/cars/<int:car_id>', methods=['GET'])
def api_get_car(car_id):
    car = Car.query.get_or_404(car_id)
    return jsonify(car_to_dict(car)), 200

# Güncelle
@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def api_update_car(car_id):
    car = Car.query.get_or_404(car_id)
    data = request.get_json(silent=True) or {}
    try:
        if 'name' in data:
            car.name = str(data['name'])
        if 'year' in data:
            car.year = int(data['year'])
        if 'mileage' in data:
            car.mileage = int(data['mileage'])
    except (ValueError, TypeError):
        return jsonify({"error": "year ve mileage sayı olmalı"}), 400

    db.session.commit()
    return jsonify(car_to_dict(car)), 200

# Sil
@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def api_delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return jsonify({"deleted": car_id}), 200

if __name__ == '__main__':
    # Geliştirme için; prod ortamda Gunicorn (CMD) kullanıyoruz
    app.run(host='0.0.0.0', debug=True)
