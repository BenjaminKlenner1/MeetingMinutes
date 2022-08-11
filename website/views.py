from pickletools import read_uint1
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Minute, Meeting
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
            meeting_id = request.form.get('meeting_id')

            if len(subject) < 1:
                flash('Minute is too short', category='error')
                pass
            else:
                new_minute = Minute(subject=subject, user_id=current_user.id, person=person, info=info, act_by=act_by, act_req=act_req, meeting_id="1")
                db.session.add(new_minute)
                db.session.commit()
                flash('Minute submitted!', category="success")
        elif request.form.get('button') == "meeting":
            flash('Meeting', category="success")
            meeting = Meeting.query.filter_by(name="Unnamed Meeting").first()

            if meeting:
                flash('Rename new meeting before creating new one!', category='error')
            else:
                new_meeting = Meeting(name="Unnamed meeting",user_id=current_user.id)
                db.session.add(new_meeting)
                db.session.commit()

        else:
            flash('Fail', category="error")

        
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

