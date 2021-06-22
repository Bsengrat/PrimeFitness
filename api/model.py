from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    weight = db.Column(db.Integer)
    Statistics = db.relationship('Statistics', backref='user', lazy='dynamic')
    stat_weight = db.relationship('stat_weight', backref='user', lazy='dynamic')


class Exercise(UserMixin, db.Model):
    Exercise_ID = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(50))
    Calories_BURN = db.Column(db.Integer)
    Name = db.Column(db.String(40))
    daily_workout = db.relationship('daily_workout', backref='exercise', lazy ='dynamic')


class ExercisePlan(UserMixin, db.Model):
    ExerciseP_ID = db.Column(db.Integer, primary_key=True)
    SetsQty = db.Column(db.Integer)



class Statistics(UserMixin, db.Model):
    Stat_id = db.Column(db.Integer, primary_key=True)
    fk__UserID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stat_Date = db.Column(db.Date)
    total_Calories_expended = db.Column(db.Integer)
    Total_Calories_Consumed = db.Column(db.Integer)
    LoggedFood = db.relationship('logged_food', backref='statistics', lazy= 'dynamic')
    DailyWorkout = db.relationship('daily_workout', backref='statistics', lazy= 'dynamic')


class daily_workout(UserMixin, db.Model):
    workout_ID = db.Column(db.Integer, primary_key=True)
    fk_stat_ID = db.Column(db.Integer, db.ForeignKey('statistics.Stat_id'), nullable=False)
    minutes = db.Column(db.Integer)
    fk_Exercise_ID = db.Column(db.Integer, db.ForeignKey('exercise.Exercise_ID'), nullable=False)


class Food(UserMixin, db.Model):
    index_id = db.Column(db.Integer, primary_key=True, nullable=False)
    Display_name = db.Column(db.String(50))
    Portion_Amount = db.Column(db.Float)
    Calories = db.Column(db.Float)
    LoggedFood = db.relationship('logged_food', backref='food', lazy ='dynamic')

class logged_food(UserMixin, db.Model):
    ID = db.Column(db.Integer, primary_key = True)
    fk_Food_Index = db.Column(db.Integer, db.ForeignKey('food.index_id'))
    fk_Statistics = db.Column(db.Integer, db.ForeignKey('statistics.Stat_id'))


class stat_weight(UserMixin, db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Weight = db.Column(db.Integer)
    Stat_DATE = db.Column(db.Date)
    fk_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


#when refercences daily workout sqlaclhemy converts table name to daily_workout... same with ExercisePlan...
















#CREATE TABLE EXERCISE(Exercise_ID INT PRIMARY KEY, Description VARCHAR(100), Calories_Burn INT, Name Varchar(40));
#CREATE TABLE EXERCISE_PLAN(ExercisePlan_ID INT PRIMARY KEY, SetsQty INT);
#CREATE TABLE DAILY_WORKOUT(workout_ID INT PRIMARY KEY, fk_Exercise_ID int, fk_Stat_ID int, foreign key(fk_Exercise_ID) references EXERCISE(Exercise_ID), foreign key (fk_Stat_ID) references Statistics(Stat_ID));
#CREATE TABLE INGREDIENTS(Ingredient_ID INT PRIMARY KEY, Description VARCHAR(100), Calories INT, Name Varchar(40));
#CREATE TABLE INVENTORY(Inventory_ID INT PRIMARY KEY, Name Varchar(40), Total_Calories INT, Description Varchar(100));
#CREATE TABLE INGREDIENT_LIST(Ingredient_list_id INT PRIMARY KEY, fk_Ingredient_ID INT, fk_Inventory_ID INT, foreign key(fk_Ingredient_ID) references INGREDIENTS(Ingredient_ID), foreign key(fk_Inventory_ID) references INVENTORY(Inventory_ID));
#CREATE TABLE DailyConsumption(Foodeaten_ID INT PRIMARY KEY, fk_Inventory_ID INT, foreign key(fk_Inventory_ID) references INVENTORY(Inventory_ID), Servings INT);