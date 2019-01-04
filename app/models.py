from app import app, db, search
from flask_user import UserMixin, UserManager

# Define the User Model
class User(db.Model, UserMixin):
	# User table
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
	username = db.Column(db.String(50, collation='NOCASE'), nullable=False, unique=True, server_default='')
	password = db.Column(db.String(255), nullable=False, server_default='')

    # User information (not used in this Programm version)
	first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
	last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

	# Define the relationship to Role via UserRoles
	roles = db.relationship('Role', secondary='user_roles')

# Define the Role data-model
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), server_default='user')

# Define the UserRoles association table
class UserRoles(db.Model):
	__tablename__ = 'user_roles'
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# init of tabels
db.create_all()

# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)

# Init Static User, if there are not created before
if not User.query.filter(User.username == 'admin').first():
	user = User(
		username = 'admin',
		password = user_manager.hash_password('Password1'),
    )
	user.roles.append(Role(name='Admin'))
	db.session.add(user)
