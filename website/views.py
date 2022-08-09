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
        minute = request.form.get('minute')

        if len(minute) < 1:
            flash('Minute is too short', category='error')
        else:
            new_minute = Minute(data=minute, user_id=current_user.id)
            db.session.add(new_minute)
            db.session.commit()
            flash('Minute submitted!', category="success")

    return render_template("home.html", user=current_user)

@views.route('/delte-minute', methods=['POST'])
def delete_minute():
    minute = json.loads(request.data)
    minuteId = minute['minuteId']
    minute = Minute.query.get(minuteId)
    if minute:
        if minute.user_id == current_user.id:
            db.session.delete(minute)
            db.session.commit()

    return jsonify({})

