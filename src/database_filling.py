from data import goals, teachers
from app import db
from models import Teacher, Goal


for i in goals:
    goal = Goal(
        id = i['id'],
        name = i['goal'],
        description = i['description'],
        icon = i['icon']
    )
    db.session.add(goal)
db.session.commit()

for i in teachers:
    teacher = Teacher(
        id = i['id'],
        name = i['name'],
        about = i['about'],
        rating = i['rating'],
        picture = i['picture'],
        price = i['price'],
        free = i['free']
    )
    for j in i['goals']:
        teacher.goals.append(db.session.query(Goal).filter(Goal.name == j).first())
    db.session.add(teacher)

db.session.commit()
