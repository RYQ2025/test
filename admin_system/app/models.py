from . import db # Import db from app package
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), nullable=False, default='submitter') # 'submitter', 'auditor', 'expert'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # User as a submitter of data
    submissions = db.relationship('DataSubmission', foreign_keys='DataSubmission.submitter_id', back_populates='submitter_user', lazy='dynamic')

    # User as an auditor of data
    # Using a different relationship name on User side if a user can audit multiple submissions
    audited_submissions_rel = db.relationship('DataSubmission', foreign_keys='DataSubmission.last_auditor_id', back_populates='auditor_user', lazy='dynamic')

    # User as an expert reviewer of data
    expert_reviewed_submissions_rel = db.relationship('DataSubmission', foreign_keys='DataSubmission.expert_id', back_populates='expert_user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

class DataSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='SUBMITTED', index=True)
    ai_score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    submitter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_auditor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    audit_notes = db.Column(db.Text, nullable=True)
    expert_notes = db.Column(db.Text, nullable=True)

    # Relationships from DataSubmission back to User
    submitter_user = db.relationship('User', foreign_keys=[submitter_id], back_populates='submissions')
    auditor_user = db.relationship('User', foreign_keys=[last_auditor_id], back_populates='audited_submissions_rel')
    expert_user = db.relationship('User', foreign_keys=[expert_id], back_populates='expert_reviewed_submissions_rel')


    def __repr__(self):
        return f'<DataSubmission {self.id} ({self.status}) by User {self.submitter_id}>'

from app import login_manager # login_manager instance from app/__init__.py
# User class is already defined in this file (app.models.User)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
