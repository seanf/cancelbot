#!/usr/bin/python

from distutils.core import setup

setup(name='DictService',
      version='1.0.0',
      description='aonaware DictService',
      long_description='class for aonware DictService generated by ZSI',
      author='Jason Powell',
      author_email='jtpowell@users.sourceforge.net',
      license='GPL',
      url='http://cancelbot.sourceforge.net',
      packages = [''],
      platform = 'any',
      extra_path = 'cancelbot',
      py_modules=['DictService_client', 'DictService_server', 'DictService_types'],
     )
