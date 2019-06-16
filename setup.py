LONG_DESCRIPTION = """
IPython Vega
============

IPython/Jupyter notebook module for `Vega <https://github.com/vega/vega/>`_
and `Vega-Lite <https://github.com/vega/vega-lite/>`_.
Notebooks with embedded visualizations can be viewed on github and nbviewer.

For more information, see https://github.com/vega/ipyvega.

Installation Notes
------------------
When installing from PyPI, extra steps may be required to enable the Jupyter
notebook extension. For more information, see the
`github page <https://github.com/vega/ipyvega>`_.
"""

DESCRIPTION         = "IPyVega: An IPython/Jupyter widget for Vega 5 and Vega-Lite 3"
NAME                = "vega"
PACKAGES            = ['vega',
                       'vega.tests']
PACKAGE_DATA        = {'vega': ['static/*.js',
                                'static/*.js.map',
                                'static/*.html']}
AUTHOR              = 'Dominik Moritz'
AUTHOR_EMAIL        = 'domoritz@gmail.com'
URL                 = 'http://github.com/vega/ipyvega'
DOWNLOAD_URL        = 'http://github.com/vega/ipyvega'
LICENSE             = 'BSD 3-clause'
DATA_FILES          = [
                            ('share/jupyter/nbextensions/jupyter-vega', [
                             'vega/static/index.js',
                             'vega/static/index.js.map',
                             'vega/static/widget.js',
                             'vega/static/widget.js.map',
                            ]),
                            ('etc/jupyter/nbconfig/notebook.d' , ['vega.json'])
                        ]
ENTRY_POINTS        = {'altair.vegalite.v3.renderer': ['notebook=vega.vegalite:entry_point_renderer'],
                       'altair.vega.v5.renderer': ['notebook=vega.vega:entry_point_renderer']
                      }
EXTRAS_REQUIRE      = {'widget': ['ipywidgets']}


import io
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py

    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = version('vega/__init__.py')


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=PACKAGES,
      package_data=PACKAGE_DATA,
      data_files=DATA_FILES,
      entry_points=ENTRY_POINTS,
      extras_require=EXTRAS_REQUIRE,
      include_package_data=True,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'],
     )
