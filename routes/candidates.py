import os
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from models import db, Candidate, StageHistory
from services.candidate_service import create_candidate, advance_candidate_stage, get_candidate_stage_duration

bp = Blueprint('candidates', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def dashboard():
    candidates = Candidate.query.all()
    pipeline = {
        'Applied': [],
        'Screening': [],
        'Interview': [],
        'Offer': [],
        'Hired': [],
        'Rejected': []
    }
    
    counts = {stage: 0 for stage in pipeline}
    
    for c in candidates:
        if c.current_stage in pipeline:
            pipeline[c.current_stage].append(c)
            counts[c.current_stage] += 1
            
    recent_activity = StageHistory.query.order_by(StageHistory.timestamp.desc()).limit(10).all()
            
    return render_template('dashboard.html', 
                           pipeline=pipeline, 
                           counts=counts,
                           recent_activity=recent_activity)

@bp.route('/candidate/<int:candidate_id>')
def candidate_detail(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    history = StageHistory.query.filter_by(candidate_id=candidate_id).order_by(StageHistory.timestamp.desc()).all()
    duration = get_candidate_stage_duration(candidate_id)
    
    return render_template('candidate_detail.html', candidate=candidate, history=history, duration=duration)

@bp.route('/candidate/add', methods=['POST'])
def add_candidate():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    role = request.form.get('role')
    notes = request.form.get('notes')
    
    if 'resume' not in request.files:
        msg = "Resume PDF file is mandatory."
        if hasattr(request, 'is_json') and request.is_json:
            return jsonify({'success': False, 'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('candidates.dashboard'))

    file = request.files['resume']
    if not file or file.filename == '':
        msg = "Resume PDF file is mandatory."
        if hasattr(request, 'is_json') and request.is_json:
            return jsonify({'success': False, 'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('candidates.dashboard'))

    if not allowed_file(file.filename):
        msg = "Only PDF format files are accepted for resumes."
        if hasattr(request, 'is_json') and request.is_json:
            return jsonify({'success': False, 'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('candidates.dashboard'))

    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'resumes')
    os.makedirs(upload_folder, exist_ok=True)
    
    filename = secure_filename(file.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    resume_url = f"/static/uploads/resumes/{unique_filename}"
    
    try:
        new_candidate = create_candidate(name, email, phone, role, resume_url, notes)
        if hasattr(request, 'is_json') and request.is_json:
            return jsonify({'success': True, 'candidate': new_candidate.to_dict()}), 201
        flash(f'Successfully added candidate {name}', 'success')
        return redirect(url_for('candidates.dashboard'))
    except Exception as e:
        if hasattr(request, 'is_json') and request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        flash(f'Error adding candidate: {str(e)}', 'error')
        return redirect(url_for('candidates.dashboard'))

@bp.route('/candidate/<int:candidate_id>/stage', methods=['POST'])
def change_stage(candidate_id):
    next_stage = request.form.get('next_stage')
    actor = request.form.get('actor', 'Recruiter')
    
    try:
        advance_candidate_stage(candidate_id, next_stage, actor)
        
        if request.headers.get('Accept') == 'application/json' or (hasattr(request, 'is_json') and request.is_json):
            return jsonify({'success': True})
            
        flash('Stage updated successfully', 'success')
        return redirect(url_for('candidates.candidate_detail', candidate_id=candidate_id))
    except ValueError as e:
        if request.headers.get('Accept') == 'application/json' or (hasattr(request, 'is_json') and request.is_json):
            return jsonify({'success': False, 'error': str(e)}), 400
            
        flash(str(e), 'error')
        return redirect(url_for('candidates.candidate_detail', candidate_id=candidate_id))
