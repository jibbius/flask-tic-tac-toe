class Config:
    pass

class DevConfig(Config):
    ENV = "Development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # We need to create a secret key, if we want to use session data.
    SECRET_KEY = "\xb8}E'8\xa2Q\xc7\xe7\x1c\x96\xae\x05V\xb9q\x89D\x90\x85\xb5\x83{\x90"
