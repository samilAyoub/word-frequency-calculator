import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # Register SQLAlchemy with app
    db.init_app(app)
    manager.run()
