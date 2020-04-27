from application import db
from sqlalchemy.sql import text

class Plant(db.Model):

    __tablename__ = 'plant'

    id = db.Column(db.Integer, primary_key = True)
    name_fin = db.Column(db.String(100), nullable = False)
    name_lat = db.Column(db.String(100), nullable = False)
    water_need = db.Column(db.String(50))
    fertilizer_need = db.Column(db.String(50))
    light_need = db.Column(db.String(50))

    users = db.relationship("PlantUser", back_populates = "plant", cascade = "all, delete-orphan")
    categories = db.relationship("PlantCategory", back_populates = "plant", cascade = "all, delete-orphan")

    def __init__(self, name_fin, name_lat, water_need, fertilizer_need, light_need):

        self.name_fin = name_fin
        self.name_lat = name_lat
        self.water_need = water_need
        self.fertilizer_need = fertilizer_need
        self.light_need = light_need

    @staticmethod
    def find_plant_by_name(name_fin):

        stmt = text("SELECT * FROM Plant"
                    " WHERE LOWER(Plant.name_fin) = :name_fin").params(name_fin = name_fin.lower())

        response = []
        res = db.engine.execute(stmt)
        for row in res:
            print(row)
            response.extend(row)
        return response

    @staticmethod
    def all_plants_number():

        stmt = text("SELECT COUNT(Plant.id) FROM Plant")

        res = db.engine.execute(stmt)
        for row in res:
            number = row[0]
        return number

    #Tämän kyselyn olisi voinut tehdä helpommin laskemalla PlantUser-taulun rivit, mutta jotta sain tehtyä pakolliset monta taulua yhdistävät järkevät yhteenvetokyselyt, jouduin tekemään tämän "vaikeamman kautta"
    @staticmethod
    def user_plants_number(current_id):

        stmt = text("SELECT COUNT(Plant.id) FROM Plant"
                    " LEFT JOIN PlantUser ON Plant.id = PlantUser.plant_id"
                    " LEFT JOIN Account ON PlantUser.user_id = Account.id"
                    " WHERE Account.id = :current").params(current = current_id)
        res = db.engine.execute(stmt)
        for row in res:
            number = row[0]
        return number

class PlantUser(db.Model):

    __tablename__ = 'plantuser'

    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key = True)

    last_watered = db.Column(db.Date)
    last_fertilized = db.Column(db.Date)

    plant = db.relationship("Plant", back_populates = "users")
    user = db.relationship("User", back_populates = "plants")

    def __init__(self, plant, user):

        self.plant = plant
        self.user = user

    @staticmethod
    def user_plants(current_id):

        stmt = text("SELECT Plant.id, PlantUser.last_watered, PlantUser.last_fertilized FROM Plant"
                    " LEFT JOIN PlantUser ON PlantUser.plant_id = Plant.id"
                    " LEFT JOIN Account ON Account.id = PlantUser.user_id"
                    " WHERE Account.id = :current").params(current = current_id)

        array = []
        res = db.engine.execute(stmt)
        for row in res:
            sublist = []
            sublist.append(row[0])
            sublist.append(row[1])
            sublist.append(row[2])
            print(sublist)
            array.append(sublist)
        return array

class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(100), nullable = False)

    plants = db.relationship("PlantCategory", back_populates = "category", cascade = "all, delete-orphan")

    def __init__(self, name, description):

        self.name = name
        self.description = description
    @staticmethod
    def categories_number():

        stmt = text("SELECT COUNT(Category.id) FROM Category")

        res = db.engine.execute(stmt)
        for row in res:
            number = row[0]
        return number

    #Tämänkin kyselyn olisi toki voinut tehdä laskemalla PlantCategoryn rivit
    @staticmethod
    def category_plants_number(category_id):

        stmt = text("SELECT COUNT(Plant.id) FROM Plant"
                    " LEFT JOIN PlantCategory ON Plant.id = PlantCategory.plant_id"
                    " LEFT JOIN Category ON PlantCategory.category_id = Category.id"
                    " WHERE Category.id = :category_id").params(category_id = category_id)

        res = db.engine.execute(stmt)
        for row in res:
            number = row[0]
        return number

    @staticmethod
    def category_query():

        return Category.query

class PlantCategory(db.Model):

    __tablename__ = 'plantcategory'

    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key = True)

    plant = db.relationship("Plant", back_populates = "categories")
    category = db.relationship("Category", back_populates = "plants")

    def __init__(self, plant, category):
        self.plant = plant
        self.category = category
