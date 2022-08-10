from config import DevConfig
from webapp import create_app

if __name__ == '__main__':

    config = DevConfig()
    flask_app = create_app(config)
    flask_app.run()

