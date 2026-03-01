
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from models import db, Ticket, Comment
from werkzeug.utils import secure_filename
import os
bp = Blueprint('tickets', __name__)
UPLOAD_FOLDER = os.path.join('static','uploads')
ALLOWED = set(['png','jpg','jpeg','gif','pdf','txt'])
def allowed_file(filename): return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED
@bp.route('/')
@login_required
def index():
    if current_user.role in ('admin','agent'):
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        tickets = Ticket.query.filter_by(customer_id=current_user.id).order_by(Ticket.created_at.desc()).all()
    return render_template('ticket_list.html', tickets=tickets)
@bp.route('/ticket/new', methods=['GET','POST'])
@login_required
def new_ticket():
    if request.method=='POST':
        title=request.form.get('title'); description=request.form.get('description'); category=request.form.get('category'); priority=request.form.get('priority') or 'Medium'
        f=request.files.get('attachment'); filename=None
        if f and allowed_file(f.filename):
            filename=secure_filename(f.filename); f.save(os.path.join(UPLOAD_FOLDER, filename))
        t=Ticket(title=title,description=description,category=category,priority=priority,customer_id=current_user.id,attachments=filename)
        db.session.add(t); db.session.commit(); flash('Ticket created','success'); return redirect(url_for('tickets.index'))
    return render_template('ticket_form.html')
@bp.route('/ticket/<int:ticket_id>', methods=['GET','POST'])
@login_required
def ticket_detail(ticket_id):
    t=Ticket.query.get_or_404(ticket_id)
    if request.method=='POST':
        body=request.form.get('body'); c=Comment(ticket_id=t.id,author_id=current_user.id,body=body); db.session.add(c); db.session.commit(); flash('Comment added','success'); return redirect(url_for('tickets.ticket_detail', ticket_id=t.id))
    return render_template('ticket_detail.html', ticket=t)
@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
