from flask_script import Manager

from miniapp.app import create_app

app = create_app('miniapp')
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
