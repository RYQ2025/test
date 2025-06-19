from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import DataSubmissionForm
from app.models import DataSubmission
from app import db
from app.auth.decorators import roles_required

@bp.route('/')
@bp.route('/index')
@login_required # Protect this route
def index():
    return render_template('main/index.html', title='Dashboard')

@bp.route('/submit_data', methods=['GET', 'POST'])
@login_required
@roles_required('submitter')
def submit_data():
    form = DataSubmissionForm()
    if form.validate_on_submit():
        submission = DataSubmission(
            data_content=form.data_content.data,
            submitter_id=current_user.id, # Make sure current_user is available
            status='SUBMITTED'
        )
        db.session.add(submission)
        db.session.commit()
        flash('Your data has been submitted successfully!', 'success')
        return redirect(url_for('main.index')) # Or a page showing their submissions
    return render_template('main/submit_data.html', title='Submit New Data', form=form)
