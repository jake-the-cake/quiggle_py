from setuptools import setup, find_packages

setup(
	name='quiggle',
	version='0.1.0',
	packages=find_packages(),
	install_requires=[
			'click'
	],
	entry_points={
			'console_scripts': [
					'rundev = dev.run:Web_Server' 
			],
	},
	author='Jason Thompson',
	author_email='jason@peakboundjourneys.com',
	description='A Python web framework with dev tools for backend Python as well as frontend JavaScript',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/jake-the-cake/quiggle_py.git',
	classifiers=[
			'Programming Language :: Python :: 3',
			'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
			'Operating System :: OS Independent',
	],
	python_requires='>=3.6',
)