#!/usr/bin/env python

from setuptools import setup

setup(
	name='TheHitList',
	description='Python library that wraps The Hit List\'s AppleScript api using appscript',
	author='Paul Traylor',
	url='http://github.com/kfdm/thehitlist/',
	version='0.2',
	packages=['TheHitList'],
	entry_points={
		'console_scripts': [
			'thl = thl:main'
		]
	}
)
