import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-svg-fields',
    version = '0.1',
    packages = ['svg_fields'],
    include_package_data = True,
    license = 'Apache License, Version 2.0', 
    description = 'SVG Fields integrated in django',
    long_description = README,
    url = 'https://github.com/hisie/django_svg_fields',
    author = 'hisie',
    author_email = 'dcebrian@serincas.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)