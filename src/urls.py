import random
import json

from flask import render_template, request, redirect, url_for, session

import src.constants as constants
from src.forms import GoalForm, RequestForm, BookingForm
from src.app import app, db
from src.models import Goal, Teacher


@app.route('/')
def main_view():
    """Main page"""

    context = {
        'goals': Goal.query.all(),
        'teachers': Teacher.query.order_by(Teacher.rating.desc()).limit(5)
    }
    return render_template('index.html', context=context)


@app.route('/all/', methods=['GET', 'POST'])
def all_teachers_view():
    """Page with all the teachers profiles"""

    form = GoalForm()

    context = {
        'teachers': Teacher.query.all(),
        'form': form
    }

    if request.method == 'POST':
        if form.goal.data == 'random':
            teachers = Teacher.query.all()
            random.shuffle(teachers)
            context['teachers'] = teachers
        elif form.goal.data == 'the_best':
            context['teachers'] = Teacher.query.order_by(
                Teacher.rating.desc()
            ).all()
        elif form.goal.data == 'expensive':
            context['teachers'] = Teacher.query.order_by(
                Teacher.price.desc()
            ).all()
        elif form.goal.data == 'cheap':
            context['teachers'] = Teacher.query.order_by(
                Teacher.price
            ).all()

    return render_template('all.html', context=context)


@app.route('/goals/<goal>/')
def choose_goal_view(goal):
    """Page with teachers sorted by the goal"""
    
    teachers = []
    for t in Teacher.query.all():
        if goal in [i.name for i in t.goals]:
            teachers.append(t)

    context = {
        'goal': Goal.query.filter(Goal.name == goal).first(),
        'teachers': teachers
    }
    
    return render_template('goal.html', context=context)


@app.route('/profiles/<int:teacher_id>/')
def teacher_profile_view(teacher_id):
    """Page for current teacher profile"""

    context = {
        'days': constants.days,
        'teacher': Teacher.query.get_or_404(teacher_id),
        'goals': Teacher.query.get(teacher_id).goals
    }

    return render_template('profile.html', context=context)


@app.route('/request/', methods=['GET', 'POST'])
def request_view():
    """Page for teacher selection form"""

    form = RequestForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            session['data'] = form.data
            return redirect(url_for('request_done_view'))

    return render_template('request.html', form=form)


@app.route('/request_done/')
def request_done_view():
    """Page for redirect after filling in the request form"""

    goal = Goal.query.filter(Goal.name == session['data']['goal']).first()
    context = {
        'data': session['data'],
        'goal': goal
    }

    return render_template('request_done.html', context=context)


@app.route('/booking/<int:teacher_id>/<day>/<time>/', methods=['GET', 'POST'])
def booking_view(teacher_id, day, time):
    """Page for booking the teacher for current day and current time"""

    form = BookingForm(
        teacher=teacher_id,
        day=day,
        time=time
    )

    if request.method == 'POST':
        if form.validate_on_submit():
            session['day'] = constants.days[form.day.data]
            session['time'] = form.time.data
            session['name'] = form.name.data
            session['phone'] = form.phone.data
            return redirect(url_for('booking_done_view'))

    context = {
        'teacher': Teacher.query.get(teacher_id),
        'day': constants.days[day],
        'time': time,
        'form': form
    }

    return render_template('booking.html', context=context)


@app.route('/booking_done/')
def booking_done_view():
    """Page for redirect after filling in the booking form"""

    context = {
        'day': session['day'],
        'time': session['time'],
        'name': session['name'],
        'phone': session['phone']
    }

    return render_template('booking_done.html', context=context)