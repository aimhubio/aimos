import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

version_file = os.path.join(here, 'aimos_ui/VERSION')
with open(version_file) as vf:
    __version__ = vf.read().strip()

# Package meta-data.
NAME = 'aimos-ui'
DESCRIPTION = 'AimOS UI'
VERSION = __version__


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


# These are symlinks to main files
files = package_files('aimos_ui/build')
files.append('../aimos_ui/VERSION')

setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    packages=['aimos_ui'],
    package_data={'aimos_ui': files}
)
