
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Ticket, User
from utils.emailer import send_email_console
bp = Blueprint('admin', __name__, url_prefix='/admin')
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required','danger'); return redirect(url_for('auth.login'))
        return fn(*args, **kwargs)
    return wrapper
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all(); agents = User.query.filter(User.role=='agent').all(); return render_template('admin_dashboard.html', tickets=tickets, agents=agents)
@bp.route('/assign', methods=['POST'])
@login_required
@admin_required
def assign_ticket():
    ticket_id=int(request.form.get('ticket_id')); agent_id=int(request.form.get('agent_id'))
    t=Ticket.query.get(ticket_id); a=User.query.get(agent_id)
    if not t or not a: flash('Invalid ticket or agent','danger'); return redirect(url_for('admin.dashboard'))
    t.agent_id=a.id; t.status='In Progress'; db.session.add(t); db.session.commit(); send_email_console(a.email, f'Ticket Assigned - #{t.id}', f'You have been assigned ticket #{t.id}'); flash('Ticket assigned','success'); return redirect(url_for('admin.dashboard'))
@bp.route('/change_status', methods=['POST'])
@login_required
@admin_required
def change_status():
    ticket_id=int(request.form.get('ticket_id')); status=request.form.get('status'); t=Ticket.query.get(ticket_id)
    if not t: flash('Invalid ticket','danger'); return redirect(url_for('admin.dashboard'))
    t.status=status; db.session.add(t); db.session.commit();
    if t.agent: send_email_console(t.agent.email, f'Ticket Status Updated - #{t.id}', f'Ticket #{t.id} status changed to {status}')
    flash('Status updated','success'); return redirect(url_for('admin.dashboard'))
