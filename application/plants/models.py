from application import db

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    nimi_lat = db.Column(db.String(100), nullable=False)
    vedentarve = db.Column(db.String(50))
    lannoituksentarve = db.Column(db.String(50))
    valontarve = db.Column(db.String(50))

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, nimi, nimi_lat, vedentarve, lannoituksentarve, valontarve):
        self.nimi = nimi
        self.nimi_lat = nimi_lat
        self.vedentarve = vedentarve
        self.lannoituksentarve = lannoituksentarve
        self.valontarve = valontarve
