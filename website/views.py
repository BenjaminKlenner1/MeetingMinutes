from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Minute
from . import db
import json

views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():
    if request.method == 'POST':
        subject = request.form.get('subject')
        person = request.form.get('person')
        info = request.form.get('info')
        act_by = request.form.get('act_by')
        act_req = request.form.get('act_req')
        meeting_id = request.form.get('meeting_id')

        if len(subject) < 1:
            flash('Minute is too short', category='error')
        else:
            new_minute = Minute(subject=subject, user_id=current_user.id, person=person, info=info, act_by=act_by, act_req=act_req, meeting_id=meeting_id)
            db.session.add(new_minute)
            db.session.commit()
            flash('Minute submitted!', category="success")
    else:
        meeting_id = 1


    return render_template("home.html", user=current_user, meeting=meeting_id)

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

