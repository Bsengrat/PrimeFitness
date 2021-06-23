from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from . import db
from .model import User, Food, Statistics, Exercise, stat_weight, daily_workout, logged_food
from datetime import datetime, date, timedelta
import re


    
# .open E:/PrimeFitness/api/database.db use this when testing out sqlite3... 
# sqlite3.exe is located in E:/sqlite3


main = Blueprint('main', __name__)

global isLog
global today
today = date.today()

isLog = False

@main.route('/')
def index():
    global isLog
    return render_template('index.html', isLogin= isLog)

@main.route('/main')
def changeLog():
    global isLog
    isLog = False
    return render_template('index.html', isLogin = isLog)

@main.route('/profile')
@login_required
def profile():
    global isLog
    isLog = True
    push_st_date = []
    combine_date_weight = {} 
    calories_dict = {}
    cal_consumed_list = {} 
    cal_expended_list = {}
    stat = Statistics.query.all()
    user_stat_weight = stat_weight.query.all()
    avg_BMR = 1600 
    weeklength = 7

    #gets the past 7 days of progess if there is any...
    for i in range(weeklength):
        pastdate = str(datetime.now() - timedelta(days = i))
        push_st_date.append(pastdate[0:10])

    #sorting list to to make sure the dates are in correct order from left-right...
    push_st_date.sort(reverse=False)
    
    #logging actual user weight into graphs...
    for userweight in  user_stat_weight:
        totalcal = 0
        for date in push_st_date:
            if current_user.id == userweight.fk_id and str(userweight.Stat_DATE) == date:
                combine_date_weight[date] = userweight.Weight
    
    #to get data for the calories...
    for x in stat:
        for date in push_st_date:
            if current_user.id == x.fk__UserID and str(x.stat_Date) == date:
                cal_consumed_list[str(x.stat_Date)] = x.Total_Calories_Consumed
                cal_expended_list[str(x.stat_Date)] = x.total_Calories_expended

    print(calories_dict)
    return render_template('profile.html', name = current_user, isLogin = isLog, labels = push_st_date, 
                points = combine_date_weight, calories_consumed_chart = cal_consumed_list,
                calories_expended_chart = cal_expended_list)

@main.route('/statistics', methods=['GET'])
@login_required
def statistics():
    global isLog
    push_st_date = []
    combine_date_weight = {} 
    calories_dict = {}
    cal_consumed_list = {} 
    cal_expended_list = {}
    stat = Statistics.query.all()
    user_stat_weight = stat_weight.query.all()
    avg_BMR = 1600 
    weeklength = 7

    #gets the past 7 days of progess if there is any...
    for i in range(weeklength):
        pastdate = str(datetime.now() - timedelta(days = i))
        push_st_date.append(pastdate[0:10])

    #sorting list to to make sure the dates are in correct order from left-right...
    push_st_date.sort(reverse=False)
    
    #logging actual user weight into graphs...
    for userweight in  user_stat_weight:
        totalcal = 0
        for date in push_st_date:
            if current_user.id == userweight.fk_id and str(userweight.Stat_DATE) == date:
                combine_date_weight[date] = userweight.Weight
    
    #to get data for the calories...
    for x in stat:
        for date in push_st_date:
            if current_user.id == x.fk__UserID and str(x.stat_Date) == date:
                cal_consumed_list[str(x.stat_Date)] = x.Total_Calories_Consumed
                cal_expended_list[str(x.stat_Date)] = x.total_Calories_expended

    print(calories_dict)

    return render_template('Statistics.html', name= current_user.name, 
    isLogin = isLog, labels = push_st_date, points = combine_date_weight, calories_consumed_chart = cal_consumed_list,
                calories_expended_chart = cal_expended_list)

@main.route('/workout')
def Workout():
    return render_template('Workout.html', isLogin = isLog)

@main.route('/about')
def about():
    return render_template('about.html', isLogin = isLog)


@main.route('/logExcsel', methods = ['POST'])
def logExercise():
    selExercise = request.form.get('selectedExercise')
    numMinutes = request.form.get('numMinutes')
    Exercise_list = Exercise.query.all()
    stats = Statistics.query.all()
    kg = 0.453592
    BMR = 1600

    print(str(selExercise))
    for exercise in Exercise_list:
        if exercise.Name == str(selExercise):
            p = exercise
        else:
            print('could not find the item')
    
    for stat in stats:
        if stat.fk__UserID == current_user.id and stat.stat_Date == today:
            stat.DailyWorkout.append(daily_workout(fk_Exercise_ID = p.Exercise_ID, minutes = numMinutes))
            stat.total_Calories_expended += (p.Calories_BURN * int(numMinutes))
            db.session.commit()
            return render_template('Workout.html', isLogin = isLog)


    new_stat_record = Statistics(stat_Date = date.today(),
            total_Calories_expended = (p.Calories_BURN * int(numMinutes) + BMR), 
            Total_Calories_Consumed = 0)   
    new_stat_record.DailyWorkout.append(daily_workout(fk_Exercise_ID = p.Exercise_ID, minutes = numMinutes, isLogin = isLog))
    
    
    current_user.Statistics.append(new_stat_record)
    db.session.add(new_stat_record)
    db.session.commit()       
    
    return render_template('Workout.html', isLogin = isLog)



@main.route('/logfoodsel', methods = ['POST'])
def logfoodselection():
    
    intial_item = request.form.get('Meal')
    stats = Statistics.query.all()
    food_list = Food.query.all()
    BMR = 1600
    gotitem = ''

    for items in food_list:
        if items.Display_name == intial_item:
            gotitem = items
            print(gotitem.Display_name)
    

    for stat in stats:
        if stat.fk__UserID == current_user.id and stat.stat_Date == today:
            stat.LoggedFood.append(logged_food(fk_Food_Index = gotitem.index_id))
            stat.Total_Calories_Consumed += gotitem.Calories
            db.session.commit()
            return render_template('Workout.html', isLogin = isLog)
        
    new_stat_record = Statistics(stat_Date = date.today(),
                        total_Calories_expended = BMR, Total_Calories_Consumed = gotitem.Calories)

    #extends the relationship between the User and Statistics class and commits it to the db...
    new_stat_record.LoggedFood.append(logged_food(fk_Food_Index = gotitem.index_id))
    current_user.Statistics.append(new_stat_record)
    db.session.add(new_stat_record)
    db.session.commit()

    return render_template('Workout.html', isLogin = isLog)


@main.route('/inputFood', methods = ['POST'])
def getFoodItems():
    foods = request.form.get('FoodItms')
    item_list = Food.query.all()

    if foods:
        food_list = list(foods.split(','))
    else:
        food_list = []
    food_output_list = {}

    for item in item_list:
        for food in food_list:
            if re.search(food.lower(), item.Display_name):
                food_output_list[item.Display_name] = item.Calories
                break
    return render_template('FoodSelection.html', food= food_output_list, isLogin = isLog)


@main.route('/NewFoodItem', methods = ['POST'])
def inputNFoodInfo():
    return render_template('newFoodItem.html')


@main.route('/postFoodItem', methods = ['POST'])
def postFoodItem():
    foodName = request.form.get('foodName')
    foodCal = request.form.get('calories')
    foods = Food.query.all()
    new_food_item = Food(Display_name = foodName.lower(), Calories = float(foodCal))


    db.session.add(new_food_item)
    db.session.commit()

    return render_template('Workout.html', isLogin = isLog)


@main.route('/inputworkout', methods = ['POST'])
def inputExercise():
    exercise = request.form.get('excItms')
    exc_list = Exercise.query.all()
    show_exc_list = {}
    kg = 0.453592


    if exercise:
        user_exc_list = list(exercise.split(','))
    else:
        user_exc_list = []
        show_exc_list = {}

    for x in exc_list:
        for item in user_exc_list:
            print(item.lower(), '   ', x.Name)
            if re.search(x.Name, item):
                mets_formula = (x.Calories_BURN * 3.5 * (current_user.weight * kg)/ 200)
                show_exc_list[x.Name] = round(mets_formula, 2)
                break

    return render_template('inputworkout.html', exc_list = show_exc_list, isLogin = isLog)


@main.route('/NewExercise', methods = ['POST'])
def ExcInfo():
    return render_template('NewExercise.html', isLogin = isLog)


@main.route("/postExcItem", methods = ['POST'])
def NewExcItem():
    exercise = request.form.get('exercise')
    description = request.form.get('description')
    mets = request.form.get('Mets')


    new_exercise = Exercise(Description = description, Name = exercise.lower(), Calories_BURN = mets)

    db.session.add(new_exercise)
    db.session.commit()

    return render_template('Workout.html', isLogin = isLog)



@main.route("/LogWeight", methods = ['POST'])
@login_required
def logWeight():
    weight = request.form.get('weight')
    user_weight = int(weight)
    statWeight_list = stat_weight.query.all()
    
    
    for stat in statWeight_list:
        if current_user.id == stat.fk_id and today == stat.Stat_DATE:
            stat.Weight = user_weight
            current_user.weight = user_weight
            db.session.commit()
            return render_template('Workout.html', isLogin = isLog)

    new_weight_record = stat_weight(Stat_DATE = date.today(), Weight = user_weight)

    #extends the relationship between the User and stat_weight class and commits it to the db...
    current_user.stat_weight.append(new_weight_record)
    db.session.add(new_weight_record)
    db.session.commit()

    return render_template('Workout.html', isLogin = isLog)


@main.route("/deletelogitem", methods = ['POST'])
@login_required
def deletePage():
    DailyFoodLog = logged_food.query.all()
    DailyExcLog = daily_workout.query.all()
    stat_Log = Statistics.query.all()
    exc_time_list = []
    exc_list = []
    show_food_list = []

 

    for stats in stat_Log:
        if current_user.id == stats.fk__UserID and stats.stat_Date == today:
            for Exc in DailyExcLog:
                if stats.Stat_id == Exc.fk_stat_ID:
                    exc_item = Exercise.query.get(Exc.fk_Exercise_ID)
                    print(Exc.workout_ID)
                    exc_list.append(exc_item.Name)
                    exc_time_list.append(Exc.minutes)
            for FoodItm in DailyFoodLog:
                print(FoodItm.fk_Food_Index)
                if stats.Stat_id == FoodItm.fk_Statistics and stats.stat_Date == today:
                        food_item = Food.query.get(FoodItm.fk_Food_Index)
                        show_food_list.append(food_item.Display_name)
                    

    return render_template('delLogitem.html', exc_list = exc_list, exc_time_list = exc_time_list, 
                                show_food_list = show_food_list, isLogin = isLog)


@main.route('/delFoodItm', methods= ['POST'])
def delfoodItm():
    food_log_itm = request.form.get('deleLoggedFood')
    stat_list = Statistics.query.all()
    get_food_log_item = Food.query.all()
    logged_food_list = logged_food.query.all()
    
    for stats in stat_list:
        if current_user.id == stats.fk__UserID and stats.stat_Date == today:
            current_stats = stats    

    for item in get_food_log_item:
        if food_log_itm == item.Display_name:
            gotItem = item
    
    for x in logged_food_list:
        print(x.fk_Food_Index, '   ', gotItem.Display_name)
        if x.fk_Food_Index == (gotItem.index_id):

            current_stats.Total_Calories_Consumed -= gotItem.Calories
            db.session.delete(x)
            db.session.commit()

            return render_template('Workout.html', isLogin = isLog)


    return render_template('Workout.html', isLogin = isLog)


    for stats in stat_list:
        if current_user.id == stats.fk__UserID and stats.stat_Date == today:
            current_stats = stats    

@main.route("/delExercise", methods = ['POST'])
def delItem():
    Exc = request.form.get('delExercise')
    time = request.form.get('timeExercise')
    DailyExcLog = daily_workout.query.all()
    Exercise_list = Exercise.query.all()
    stat_list = Statistics.query.all()
    kg = 0.453592


    for stats in stat_list:
        if current_user.id == stats.fk__UserID and stats.stat_Date == today:
            current_stats = stats


    for dailylogItm in DailyExcLog:
        for exc in Exercise_list:
            print(dailylogItm.minutes)
            if dailylogItm.fk_Exercise_ID == exc.Exercise_ID and dailylogItm.minutes == int(time):
                print('a;lfkjsa;kljfkdsjfkjjjjj')
                mets_formula = (exc.Calories_BURN * 3.5 * (current_user.weight * kg)/ 200)
                calories_Expended = mets_formula * float(time)
                current_stats.total_Calories_expended -= calories_Expended
                db.session.delete(dailylogItm)
                db.session.commit()

                return render_template('Workout.html', isLogin = isLog)
                


    return render_template('Workout.html', isLogin = isLog)
    





