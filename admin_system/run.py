from app import app, db  # Import app and db directly
from app.models import User
import click

# Note: app.cli.group is available in Flask 2.x
# For Flask 1.x, one might need to use flask.cli.AppGroup
# Assuming Flask 2.x based on requirements.txt (Flask==2.3.2)

@click.group(name='user', help="Manages users.")
def user_cli():
    pass

@user_cli.command("create")
@click.option('--username', required=True, help='The username for the new user.')
@click.option('--email', required=True, help='The email address for the new user.')
@click.option('--password', required=True, help='The password for the new user.')
@click.option('--role', default='submitter', type=click.Choice(['submitter', 'auditor', 'expert'], case_sensitive=False), help='The role of the new user.')
def create_user(username, email, password, role):
    # Commands need to run within application context to access db etc.
    with app.app_context():
        if User.query.filter_by(username=username).first():
            click.echo(f'Error: Username "{username}" already exists.')
            return
        if User.query.filter_by(email=email).first():
            click.echo(f'Error: Email "{email}" already registered.')
            return
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        click.echo(f'User "{username}" ({email}) created successfully with role "{role}".')

@user_cli.command("list")
def list_users():
    with app.app_context():
        users = User.query.all()
        if not users:
            click.echo("No users found in the database.")
            return
        click.echo("Registered Users:")
        for u in users:
            click.echo(f"  ID: {u.id}, Username: {u.username}, Email: {u.email}, Role: {u.role}")

app.cli.add_command(user_cli)

if __name__ == '__main__':
    app.run(debug=True)
