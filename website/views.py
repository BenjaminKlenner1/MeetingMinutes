from pickletools import read_uint1
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Minute
from . import db
import json

views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('button') == "minute":
            subject = request.form.get('subject')
            person = request.form.get('person')
            info = request.form.get('info')
            act_by = request.form.get('act_by')
            act_req = request.form.get('act_req')
            attendees = request.form.get('attendees')

            if len(subject) < 1:
                flash('Minute is too short', category='error')
                pass
            else:
                new_minute = Minute(subject=subject, user_id=current_user.id, person=person, info=info, act_by=act_by, act_req=act_req, attendees=attendees)
                db.session.add(new_minute)
                db.session.commit()
                flash('Minute submitted!', category="success")
       

        

    return render_template("home.html", user=current_user)

@views.route('/delete-minute', methods=['POST'])
def delete_minute():
    minute = json.loads(request.data)
    minuteId = minute['minuteId']
    minute = Minute.query.get(minuteId)
    if minute:
        if minute.user_id == current_user.id:
            db.session.delete(minute)
            db.session.commit()

    return jsonify({})



