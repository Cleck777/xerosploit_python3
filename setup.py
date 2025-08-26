#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

def read_requirements():
    """Read requirements from requirements.txt if it exists"""
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            return f.read().splitlines()
    return []

def read_long_description():
    """Read the long description from README.md"""
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "Xerosploit - A network security penetration testing framework"

setup(
    name='xerosploit',
    version='2.0.0',
    author='LionSec',
    author_email='contact@lionsec.net',
    description='A network security penetration testing framework',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/LionSec/xerosploit',
    packages=find_packages(),
    py_modules=['xerosploit', 'banner'],
    entry_points={
        'console_scripts': [
            'xerosploit=xerosploit:main',
        ],
    },
    install_requires=[
        'tabulate>=0.8.0',
        'terminaltables>=3.1.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'black>=21.0',
            'flake8>=3.8',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    keywords='security penetration-testing network hacking',
    include_package_data=True,
    package_data={
        '': ['tools/**/*', 'README.md', 'LICENSE'],
    },
    data_files=[
        ('share/xerosploit/tools', ['tools']),
    ],
)
