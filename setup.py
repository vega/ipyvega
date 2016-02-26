# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='vega',
    version='0.2',
    description='An iPython/ Jupyter widget for Vega and Vega-Lite',
    author='Dominik Moritz',
    author_email='domoritz@gmail.com',
    license='BSD-3-Clause',
    url='https://github.com/vega/ipython-vega',
    keywords='data visualization',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: BSD License'],
    packages=['vega'],
    package_data={'': ['static/*.js',
                       'static/*.css']}
)
