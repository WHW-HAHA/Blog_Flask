"""
Hanwei Wang
Time: 13-2-2020 9:33
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
# ?? what is WIN

if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig(object):
    # SECRET_KEY = os.getenv('SECRET', 'dev key')
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'site.db')
    DEBUG = True

config = {
    'development': DevelopmentConfig
}




