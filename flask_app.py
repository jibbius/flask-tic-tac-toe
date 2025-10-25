from config import DevConfig
from webapp import create_app

if __name__ == '__main__':

    config = DevConfig()
    app = create_app(config)
    app.run()

