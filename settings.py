class BlogSetting:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234@localhost/BLOG"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = 'FAKE_SECRET_KEY'
