from setuptools import setup, find_packages
import sys, os

def read(*names):
    values = dict()
    for name in names:
        filename = name+'.txt'
        if os.path.isfile(filename):
            value = open(name+'.txt').read()
        else:
            value = ''
        values[name] = value
    return values

long_description="""
%(README)s

See http://packages.python.org/django-videos/ for the full documentation

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

version = '0.3'

setup(name='django-videos',
      version=version,
      description="Add some youtube videos to your django app",
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django youtube',
      author='Bearstech',
      author_email='gpasgrimaud@bearstech.com',
      url='http://packages.python.org/django-videos/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'test_project']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [django.pluggable_app]
      djangovideos = djangovideos:pluggableapp
      """,
      )
