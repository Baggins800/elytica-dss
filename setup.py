import os
import sys

try:
    from setuptools import setup
    from setuptools_git_versioning import version_from_git

except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name = 'elytica_dss',
  version=version_from_git(),
  packages = ['elytica_dss'],
  version_config={
      "template": "{tag}",
      "dev_template": "{tag}.dev{ccount}+git.{sha}",
      "dirty_template": "{tag}.dev{ccount}+git.{sha}.dirty",
      "starting_version": "0.0.1",
      "metadata_version": "{tag}",
      "version_callback": None,
      "version_file": None,
      "count_commits_from_version_file": False
  },
  setup_requires=['setuptools-git-versioning'],
  license='GPL',
  description = 'Package for elytica service we use to build decision support systems (DSSs).',
  author = 'Ruan Luies',
  author_email = 'ruan@elytica.com',
  url = 'https://github.com/baggins800/elytica-dss',
  keywords = ['DSS', 'decision', 'support', 'system', 'mixed', 'integer', 'linear', 'programming'],
  install_requires=[  
    'requests>=1.6'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
  ],
)
