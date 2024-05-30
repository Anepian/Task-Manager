import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
    RECAPTCHA_PUBLIC_KEY = os.environ.get('6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI') or '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe') or '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')