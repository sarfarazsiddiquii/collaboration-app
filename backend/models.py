from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Workspace model
class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128), nullable=False)
    plain_code = db.Column(db.String(128), nullable=False)  # Temporary field for demonstration
    users = db.relationship('User', secondary='workspace_user', backref='workspaces')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.plain_code = password  # Store the plain text code temporarily

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Many-to-Many relationship for workspaces and users
workspace_user = db.Table(
    'workspace_user',
    db.Column('workspace_id', db.Integer, db.ForeignKey('workspace.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# Invite model
class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
    invited_at = db.Column(db.DateTime, default=datetime.utcnow)

# ScrapedContent model
class ScrapedContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
