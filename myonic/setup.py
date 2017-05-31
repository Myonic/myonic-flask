from setuptools import setup

setup(
    name='Myonic CMS',
    packages=['myonic'],
    include_package_data=True,
    #scripts=[],
    install_requires=[
        'flask',
        'flask-dance',
        'flask-sqlalchemy',
        'flask-login',
        'sqlalchemy-utils',
        'blinker',
        'flask-mail',
        'flask-wtf',
        'sqlalchemy-migrate',
        'flask-migrate',
        'flask-assets'
    ],
)
