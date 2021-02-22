from src.app import db
from sqlalchemy.dialects.postgresql import JSON


teacher_goals = db.Table(
    'teacher_goals',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goal_id', db.Integer, db.ForeignKey('goals.id'))
)


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text)
    rating = db.Column(db.Float)
    picture = db.Column(db.String(255))
    price = db.Column(db.Integer)
    goals = db.relationship(
        'Goal', 
        secondary=teacher_goals,
        back_populates='teachers'
    )
    free = db.Column(JSON)


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(255))
    icon = db.Column(db.String(255))
    teachers = db.relationship(
        'Teacher',
        secondary=teacher_goals,
        back_populates='goals'
    )
