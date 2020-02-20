"""
Hanwei Wang
Time: 12-2-2020 11:07
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""
import logging
import os
import click

from Webapp.settings import config
from flask import Flask, render_template, request

from Webapp.extensions import bootstrap, db, mail, login_manager


def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development') # get the name of development configuration

    app = Flask('Webapp')
    app.config.from_object(config[config_name])

    # register application
    register_extensions(app)
    register_blueprint(app)
    return app

def register_extensions(app):
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprint(app):
    pass


def forge():
    ''' Create fake data '''
    from Webapp.fakes import fake_admin,fake_user, fake_category, fake_deal, fake_post

    db.drop_all()
    db.create_all()

    click.echo('Generating the administrator...')
    fake_admin()

    click.echo('Generating users')
    fake_user()

    # click.echo('Generating %d categories...' % category)
    click.echo('Generating categories...')
    fake_category()

    click.echo('Generating del')

    click.echo('Generating posts...' )
    fake_post()

    click.echo('Generating deals')
    fake_deal()

    click.echo('Done.')



