from db import db

class DummyModel(db.Model):
    __tablename = 'dummy'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    string = db.Column(db.String(80), nullable=False)
    int_zahl = db.Column(db.Integer, nullable=False)
    float_zahl = db.Column(db.Float, nullable=False)
    bool = db.Column(db.Boolean)
    text = db.Column(db.Text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_string(cls, string):
        return cls.query.filter_by(string=string).first()

    @classmethod
    def find_by_userid(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
