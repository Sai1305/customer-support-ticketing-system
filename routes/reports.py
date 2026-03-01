
from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from models import Ticket, db
from sqlalchemy import func
bp = Blueprint('reports', __name__, url_prefix='/reports')
@bp.route('/data_status')
@login_required
def data_status():
    q = db.session.query(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status).all(); data = {status: count for status, count in q}; return jsonify(data)
@bp.route('/overview')
@login_required
def overview():
    return render_template('reports.html')
