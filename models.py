from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Car {self.name}>"
