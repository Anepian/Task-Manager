import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
    RECAPTCHA_PUBLIC_KEY = os.environ.get('6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI') or '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe') or '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False