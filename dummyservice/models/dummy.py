from db import db

class DummyModel(db.Model):
    __tablename = 'product'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    string = db.Column(db.String(80))
    int_zahl = db.Column(db.Integer)
    float_zahl = db.Column(db.Float)
    bool = db.Column(db.Boolean)
    text = db.Column(db.Text)

    def __init__(self,  user_id, string, int_zahl, float_zahl, bool, text):
        self.user_id = user_id
        self.string = string
        self.int_zahl = int_zahl
        self.float_zahl = float_zahl
        self.bool = bool
        self.text = text

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

    def json(self):
        return {
                'string': self.string,
                'user_id': self.user_id,
                'int_zahl': self.int_zahl,
                'float_zahl': self.float_zahl,
                'bool': self.bool,
                'text': self.text,
        }
