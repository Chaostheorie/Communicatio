from app import app, db, search
from app.mixin import SearchableMixin
from flask_user import UserMixin, UserManager

# Define custom User Model with flask_user"s UserMixin
class Users(db.Model, UserMixin):
	# User table
	__tablename__ = "Users"
	__searchable__ = ["username", "first_name", "last_name"]
	id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
	active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
	username = db.Column(db.String(50, collation="NOCASE"), nullable=False, unique=True, server_default="")
	password = db.Column(db.String(255), nullable=False, server_default="")

    # User information (not used in this Programm version)
	first_name = db.Column(db.String(100, collation="NOCASE"), nullable=False, server_default="")
	last_name = db.Column(db.String(100, collation="NOCASE"), nullable=False, server_default="")

	# Define the relationship to Role via UserRoles
	roles = db.relationship("Role", secondary="user_roles",\
		backref = db.backref( "users" ) )

	# Define the relationship for author_id in terms and entrys models
	terms = db.relationship("terms", backref="author", lazy="dynamic")
	entrys = db.relationship("entrys", backref="author", lazy="dynamic")

# Define the Role data-model
class Role(db.Model):
	__tablename__ = "roles"
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
	__tablename__ = "user_roles"
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey("Users.id", ondelete="CASCADE"))
	role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))

# Define the Entry Model with custom SearchableMixin
# creation date/ time are only for full time view
class entrys(db.Model, SearchableMixin):
	__tablename__ = "entrys"
	__searchable__ = ["name", "content"]
	id = db.Column(db.Integer(), primary_key=True, unique=True)
	name = db.Column(db.String(150))
	author_id = db.Column(db.Integer(), db.ForeignKey("Users.id", ondelete="CASCADE"))
	creation_date = db.Column(db.String(20))
	creation_time = db.Column(db.String(20))
	content = db.Column(db.String(150))

# Define the Term Model with custom SearchableMixin
# creation date/ time are only for full view
class terms(db.Model, SearchableMixin):
	__tablename__ = "terms"
	__searchable__ = ["name", "destination_day", "description"]
	id = db.Column(db.Integer(), primary_key=True, unique=True)
	name = db.Column(db.String(150))
	# author is only for traceability
	author_id = db.Column(db.Integer(), db.ForeignKey("Users.id", ondelete="CASCADE"))
	creation_date = db.Column(db.String(20))
	creation_time = db.Column(db.String(20))
	destination_day = db.Column(db.String(20))
	description = db.Column(db.String(150))

# init of tabels
db.create_all()


# Init Static User, if there are not created before
admin_role = Role(name="Admin")
db.session.commit()
