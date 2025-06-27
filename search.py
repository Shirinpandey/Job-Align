from flask import Blueprint,render_template, request
from flask_login import current_user
from models import Job, SavedJob
from job import storefiles
from extension import db 

search =  Blueprint('search',__name__)

@search.route('job', methods = ['GET','POST'])
def job_search():
    query = request.args.get('query','')
    results = []
    query = query.strip()
    if query:
        results = Job.query.filter(Job.job_title.ilike(f'%{query}%') | 
                                  Job.location.ilike(f'%{query}%') |
                                  Job.company.ilike(f'%{query}%')).all()
    else:
        results = Job.query.all()
    
        
    return render_template('search.html', jobs = results)

def load_jobs_once():
    new_file = storefiles()
    for job in new_file:
        existing_job = Job.query.filter_by(job_title=job['title'], company=job['company']).first()
        if not existing_job:
            skills_str = ", ".join(job['skills'])
            job_entry = Job(job_title=job['title'], location=job['location'], company=job['company'], description=job['description'], skills=skills_str, apply = job['apply'])
            db.session.add(job_entry)
    db.session.commit()

from flask import request, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Job, SavedJob
from extension import db

@search.route('saved_jobs', methods=['GET', 'POST'])
@login_required
def save_jobs():
    if request.method == 'POST':
        job_id = request.form.get('job_id')
        user_id = current_user.id

        if job_id:
            existing = SavedJob.query.filter_by(job_id=job_id, user_id=user_id).first()
            if not existing:
                saved_job = SavedJob(job_id=job_id, user_id=user_id)
                db.session.add(saved_job)
                db.session.commit()
            return redirect(url_for('search.save_jobs'))  

    user_id = current_user.id
    saved_jobs = SavedJob.query.filter_by(user_id=user_id).all()
    jobs = [Job.query.get(saved.job_id) for saved in saved_jobs]

    return render_template('saved_jobs.html', save_jobs=jobs)
