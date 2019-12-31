# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="appendorgheading",
    version="2019.12.31.1",
    description="Append a new Org mode heading to an existing Org mode file",
    author="Karl Voit",
    author_email="tools@Karl-Voit.at",
    url="https://github.com/novoid/appendorgheading",
    download_url="https://github.com/novoid/appendorgheading/zipball/master",
    keywords=["org mode", "orgmode", "CLI", "logging", "shell"],
    packages=find_packages(), # Required
    package_data={},
    install_requires=["orgformat"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        ],
    entry_points={  # Optional
        'console_scripts': [
            'appendorgheading=appendorgheading:main'
        ],
    },
    long_description="""This tool appends Org mode formatted headings to existing Org mode files.

The author is using this to log events to some kind of 'errors.org' which is part
of his Org mode agenda.

Command line parameters override configuration file entries.
- Hosted and documented on github: https://github.com/novoid/appendorgheading
"""
)
