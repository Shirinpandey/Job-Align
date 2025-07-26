from flask import Blueprint,render_template, request, redirect, url_for, flash
from models import Job, SavedJob
from job import storefiles
from extension import db 
from flask_login import login_required, current_user
from sqlalchemy import or_, func



search =  Blueprint('search',__name__)

@search.route('/job', methods = ['GET','POST'])
def job_search():
    query = request.args.get('query', '').strip().lower()
    results = []

    if query:
        query = query.lower()

        results = Job.query.filter(
            or_(
                func.lower(Job.job_title).like(f"%{query}%"),
                func.lower(Job.company).like(f"%{query}%"),
                func.lower(Job.location).like(f"%{query}%"),
                func.lower(Job.skills).like(f"%{query}%")  # Search for the query in skills field
            )
        ).all()
    else:
        results = Job.query.all()

    for job in results:
        job.skills_display = [s.strip() for s in job.skills.split(',')] if job.skills else []

    return render_template('search.html', jobs = results)

# def load_jobs_once():
#     new_file = storefiles()
#     for job in new_file:
#         existing_job = Job.query.filter_by(job_title=job['title'], company=job['company']).first()
#         if not existing_job:
#             skills_str = ", ".join(job['skills'])
#             job_entry = Job(job_title=job['title'], location=job['location'], company=job['company'], description=job['description'], skills=skills_str, apply = job['apply'])
#             db.session.add(job_entry)
#     db.session.commit()


from flask import request, jsonify

@search.route('save-job', methods=['POST'])
@login_required
def save_jobs():
    user_id = current_user.id
    print("Incoming request to /save-job")

    try:
        data = request.get_json()  # this reads the JSON body sent from fetch()
        print("Received data:", data)

        job_id = data.get('job_id')#extracts the job_id from the data
        action = data.get('action')
    
        if not job_id or not action:
            return jsonify({"message": "Job ID or action not provided."}), 400

        if action == 'save':
            existing_job = SavedJob.query.filter_by(job_id=job_id, user_id=user_id).first()
            if existing_job:
                return jsonify({'message':'Job Already Saved'})
            job = Job.query.get(job_id)
            if not job:
                return jsonify({"message": "Job not found."}), 404
            saved_job = SavedJob(job_id=job.id, user_id=user_id)
            db.session.add(saved_job)
            db.session.commit()

            return jsonify({"message": "Job saved successfully!"})
        elif action == 'remove':
            existing_job = SavedJob.query.filter_by(job_id=job_id, user_id=user_id).first()
            if existing_job:
                db.session.delete(existing_job)
                db.session.commit()
                return jsonify({'message':'Job Removed Successfully'})


        return jsonify({"message": "Invalid action."}), 400
    
    
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



@search.route('saved_jobs', methods=['GET', 'POST'])
@login_required
def display_save_jobs():
    user_id = current_user.id

    saved_jobs = SavedJob.query.filter_by(user_id=user_id).all()
    jobs = [Job.query.get(saved.job_id) for saved in saved_jobs]

    return render_template('saved_jobs.html', save_jobs=jobs)



@search.route('/update-status', methods=['POST'])
def update_status():
    new_status = request.form.get('status')
    job_id = request.form.get('job_id')

    job = Job.query.get(job_id)  

    if job:
        job.status = new_status  
        db.session.commit()      
        return '', 204           
    else:
        return "Job not found", 404
