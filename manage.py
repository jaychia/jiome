from app import app
from flask.ext.script import Manager
from app import db

#Initializing manager
manager = Manager(app)
from app.main import main as main_blueprint
app.register_blueprint(main_blueprint)

@manager.command
def create(default_data=True, sample_data=False):
	"Creates database tables from sqlalchemy models"
	db.create_all()


if __name__ == "__main__":
	manager.run()