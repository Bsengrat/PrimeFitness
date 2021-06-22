CREATE DATABASE IF NOT EXISTS FITDATA;

use FITDATA;
select database();
show tables;
select * from User;
#CREATE TABLE User(UserID INT PRIMARY KEY, username VARCHAR(20), Email VARCHAR(30));
#CREATE TABLE Statistics(Stat_ID INT PRIMARY KEY, fk_UserID int, foreign key (fk_UserID) references User(UserID), stat_Date DATE, total_Calories_expended INT, Total_Calories_Consumed INT);
#CREATE TABLE EXERCISE(Exercise_ID INT PRIMARY KEY, Description VARCHAR(100), Calories_Burn INT, Name Varchar(40));
#CREATE TABLE EXERCISE_PLAN(ExercisePlan_ID INT PRIMARY KEY, SetsQty INT);
#CREATE TABLE DAILY_WORKOUT(workout_ID INT PRIMARY KEY, fk_Exercise_ID int, fk_Stat_ID int, foreign key(fk_Exercise_ID) references EXERCISE(Exercise_ID), foreign key (fk_Stat_ID) references Statistics(Stat_ID));
#CREATE TABLE INGREDIENTS(Ingredient_ID INT PRIMARY KEY, Description VARCHAR(100), Calories INT, Name Varchar(40));
#CREATE TABLE INVENTORY(Inventory_ID INT PRIMARY KEY, Name Varchar(40), Total_Calories INT, Description Varchar(100));
#CREATE TABLE INGREDIENT_LIST(Ingredient_list_id INT PRIMARY KEY, fk_Ingredient_ID INT, fk_Inventory_ID INT, foreign key(fk_Ingredient_ID) references INGREDIENTS(Ingredient_ID), foreign key(fk_Inventory_ID) references INVENTORY(Inventory_ID));
#CREATE TABLE DailyConsumption(Foodeaten_ID INT PRIMARY KEY, fk_Inventory_ID INT, foreign key(fk_Inventory_ID) references INVENTORY(Inventory_ID), Servings INT);

show tables;
