import os
import sys

try:
    from setuptools import setup
    from version import get_git_version

except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = 'elytica-dss',
  packages = ['elytica-dss'],
  version_format='{tag}',
  license='GPL',
  description = 'Package for elytica service we use to build decision support systems (DSSs).',
  author = 'Ruan Luies',
  author_email = 'ruan@elytica.com',
  url = 'https://github.com/baggins800/elytica-dss',
  keywords = ['DSS', 'decision', 'support', 'system', 'mixed', 'integer', 'linear', 'programming'],
  setup_requires=['setuptools-git-version'],
  install_requires=[  
    'requests>=1.6', 'json'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
  ],
)