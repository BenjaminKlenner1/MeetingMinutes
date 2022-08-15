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
    print("Home")

    meeting_id = request.form.get('currentMeeting')
    if meeting_id == None or meeting_id == "":
        meeting_id = Meeting.query.filter_by(user_id=current_user.id).first().id

    if request.method == 'POST':
        if request.form.get('button') == "minute":
            subject = request.form.get('subject')
            person = request.form.get('person')
            info = request.form.get('info')
            act_by = request.form.get('act_by')
            act_req = request.form.get('act_req')

            if len(subject) < 1:
                flash('Minute is too short', category='error')
                pass
            else:
                new_minute = Minute(subject=subject, user_id=current_user.id, person=person, info=info, act_by=act_by, act_req=act_req, meeting_id=meeting_id)
                db.session.add(new_minute)
                db.session.commit()
                flash('Minute submitted!', category="success")

        elif request.form.get('button') == "meeting":

            #check for meetings with default name AND matching user id
            meeting = Meeting.query.filter_by(name="Unnamed meeting").first()
            if meeting and meeting.user_id == current_user.id:
                flash('Rename new meeting before creating new one!', category='error')


            else:
                new_meeting = Meeting(name="Unnamed meeting",user_id=current_user.id)
                db.session.add(new_meeting)
                db.session.commit()

        elif request.form.get('button') == "submit-edit":
            #This needs to be selected by meetings navbar
            selected_meeting = meeting
            print(selected_meeting)
            name = request.form.get('meeting_name')
            attendees = request.form.get('attendees')
            info = request.form.get('meeting_info')

            if len(name) < 1:
                flash('Meeting name is too short', category='error')
                pass
            else:
                meeting = Meeting.query.filter_by(id=selected_meeting).first()
                meeting.name = name
                meeting.attendees = attendees
                meeting.info = info
                db.session.commit()


        elif request.form.get('button') == "delete-meeting":
            #delete meeting and matching minutes
            pass

        else:
            flash('Fail', category="error")

        

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

@views.route('/select-meeting', methods=['POST'])
def select_meeting():
    meeting = json.loads(request.data)
    meetingId = meeting['meetingId']
    meeting = Meeting.query.get(meetingId)
    if meeting:
        if meeting.user_id == current_user.id:
            print(meetingId)
            return render_template("home.html", user=current_user, meeting=meetingId)

