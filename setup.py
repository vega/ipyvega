# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='vegawidget',
    version='0.1',
    description='An IPython widget for polestar and voyager',
    author='Dominik Moritz, Kanit "Ham" Wongsuphasawat',
    author_email='domoritz@gmail.com',
    license='MIT License',
    url='https://github.com/uwdata/ipython-vega',
    keywords='data visualization',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: MIT License'],
    packages=['vegawidget'],
    package_data={'': ['static/*.js',
                       'static/*.css']}
)
