import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.normpath(os.path.join(BASE_DIR, '../')))

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from project.umg.app import create_app, db

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)
migrate = Migrate(app=app, db=db)

manager = Manager(app=app)


@manager.command
def createsuperuser():
    from project.auth.models import User

    admin = User({
        'username': 'admin',
        'password': '123qwe!@#',
        'first_name': 'Admin',
        'last_name': 'Adminian',
        'phone_number': '09353942996',
        'is_admin': True
    })

    with app.app_context():
        if not admin.check_username_exists():
            admin.save()
            print('>> Admin created successfully')
        else:
            print('>> Admin created before')


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
