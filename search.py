from flask import Blueprint,render_template, request, redirect, url_for, flash
from models import Job, SavedJob
from job import storefiles
from extension import db 
from flask_login import login_required, current_user
from sqlalchemy import or_, func



search =  Blueprint('search',__name__)

@search.route('job', methods = ['GET','POST'])
def job_search():
    query = request.args.get('query', '').strip().lower()
    results = []

    if query:
        results = Job.query.filter(
            or_(
                func.lower(Job.job_title).like(f"%{query}%"),
                func.lower(Job.company).like(f"%{query}%"),
                func.lower(Job.location).like(f"%{query}%")
            )
        ).all()
    else:
        results = Job.query.all()

    for job in results:
        job.skills_display = [s.strip() for s in job.skills.split(',')] if job.skills else []

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


@search.route('saved_jobs', methods=['GET', 'POST'])
@login_required
def display_save_jobs():
    user_id = current_user.id

    if request.method == 'POST':
        job_id = request.form.get('job_id')
        action = request.form.get('action')

        if not job_id:
            flash("No job ID provided.")
        if action == 'save':
            existing = SavedJob.query.filter_by(job_id=job_id, user_id=user_id).first()
            if not existing:
                db.session.add(SavedJob(job_id=job_id, user_id=user_id))
                db.session.commit()
                flash("Job saved!")
        elif action == 'remove':
            existing = SavedJob.query.filter_by(job_id=job_id, user_id=user_id).first()
            if existing:
                db.session.delete(existing)
                db.session.commit()
                flash("Job removed.")
    saved_jobs = SavedJob.query.filter_by(user_id=user_id).all()
    jobs = [Job.query.get(saved.job_id) for saved in saved_jobs]

    return render_template('saved_jobs.html', save_jobs=jobs)


def save_jobs(job_id,user_id):
    if job_id:
        existing = SavedJob.query.filter_by(job_id=job_id, user_id=user_id).first()
        if not existing:
            saved_job = SavedJob(job_id=job_id, user_id=user_id)
            db.session.add(saved_job)
            db.session.commit() 

def remove_job(job_id,user_id):
    if job_id:
        saved = SavedJob.query.filter_by(job_id=job_id, user_id=user_id).first()
        if saved:
            db.session.delete(saved)
            db.session.commit()

