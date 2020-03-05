"""
Hanwei Wang
Time: 20-2-2020 10:32
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
from dotenv import load_dotenv


# claim and use .env or .flaskenv as setting files
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def Forge(app):
    ''' Create fake data '''
    from Webapp.fakes import fake_admin, fake_user, fake_category, fake_deal, fake_post
    from Webapp import db
    import click

    with app.app_context(): # give sqlalchemy an app context
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

        click.echo('Generating posts...')
        fake_post()

        click.echo('Generating deals')
        fake_deal()

        click.echo('Done.')

from Webapp import create_app

app = create_app()
Forge(app)
app.run(debug = True)

