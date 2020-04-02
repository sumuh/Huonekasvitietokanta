from application import db
from sqlalchemy.sql import text

class Plant(db.Model):

    __tablename__ = 'plant'

    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    nimi_lat = db.Column(db.String(100), nullable=False)
    vedentarve = db.Column(db.String(50))
    lannoituksentarve = db.Column(db.String(50))
    valontarve = db.Column(db.String(50))

    users = db.relationship("PlantUser", back_populates="plant", cascade="all, delete-orphan")
    categories = db.relationship("PlantCategory", back_populates="plant", cascade="all, delete-orphan")

    def __init__(self, nimi, nimi_lat, vedentarve, lannoituksentarve, valontarve):
        self.nimi = nimi
        self.nimi_lat = nimi_lat
        self.vedentarve = vedentarve
        self.lannoituksentarve = lannoituksentarve
        self.valontarve = valontarve

    @staticmethod
    def find_plant_by_name(name):
        stmt = text("SELECT Plant.id FROM Plant"
                    " WHERE Plant.nimi = :name").params(name=name)

        response = []
        res = db.engine.execute(stmt)
        for row in res:
            response.append(row[0])
        return response

class PlantUser(db.Model):

    __tablename__ = 'plantuser'

    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)

    plant = db.relationship("Plant", back_populates="users")
    user = db.relationship("User", back_populates="plants")

    def __init__(self, plant, user):
        self.plant = plant
        self.user = user

    @staticmethod
    def user_plants(current_id):
        stmt = text("SELECT Plant.id, Plant.nimi FROM Plant"
                    " LEFT JOIN PlantUser ON PlantUser.plant_id = Plant.id"
                    " LEFT JOIN Account ON Account.id = PlantUser.user_id"
                    " WHERE Account.id = :current").params(current=current_id)

        response = []
        res = db.engine.execute(stmt)
        for row in res:
            response.append(row[0])
        return response

class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    kuvaus = db.Column(db.String(100), nullable=False)

    plants = db.relationship("PlantCategory", back_populates="category", cascade="all, delete-orphan")

    def __init__(self, nimi, kuvaus):
        self.nimi = nimi
        self.kuvaus = kuvaus

    @staticmethod
    def category_query():
        return Category.query

class PlantCategory(db.Model):

    __tablename__ = 'plantcategory'

    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)

    plant = db.relationship("Plant", back_populates="categories")
    category = db.relationship("Category", back_populates="plants")

    def __init__(self, plant, category):
        self.plant = plant
        self.category = category
