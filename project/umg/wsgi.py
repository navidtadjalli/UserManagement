import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.normpath(os.path.join(BASE_DIR, '../')))

from project.umg.app import create_app

application = create_app(os.environ.get('FLASK_ENV'))

if __name__ == '__main__':
    application.run()
