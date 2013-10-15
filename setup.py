#!/usr/bin/env python
from version import VERSION

from setuptools import setup

install_requires = ['lxml==3.1.0',
                    'requests==1.1.0',
                    'tox==1.4.3']

setup(name='ispdb',
      version=VERSION,
      description='Interface to Mozilla ISP database',
      author='sprt',
      author_email='hellosprt@gmail.com',
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Communications :: Email :: Email Clients (MUA)',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   # the two following have not been tested yet
                   # 'Programming Language :: Python :: 3.0',
                   # 'Programming Language :: Python :: 3.1',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: Implementation :: PyPy',
                   ],
      py_modules=['ispdb', 'version'],
      license='MIT License',
      install_requires=install_requires,
      test_suite='test')
