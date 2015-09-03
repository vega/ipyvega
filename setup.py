# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='vega',
    version='0.1',
    description='An IPython widget for vega-lite, polestar, and voyager',
    author='Dominik Moritz, Kanit "Ham" Wongsuphasawat',
    author_email='domoritz@gmail.com',
    license='MIT License',
    url='https://github.com/uwdata/ipython-vega',
    keywords='data visualization',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: BSD License'],
    packages=['vega'],
    package_data={'': ['static/*.js',
                       'static/*.css']}
)
