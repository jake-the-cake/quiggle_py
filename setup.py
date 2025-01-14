from setuptools import setup, find_packages
from quiggle.config.globals import VERSION_NUMBER

setup(
	name='quiggle',
	version=VERSION_NUMBER,
	packages=find_packages(),
	install_requires=[
			# 'click',
            'psutil'
	],
	entry_points={
			'console_scripts': [
					'createproject = quiggle.quiggle:create',
                    'quiggle = quiggle.__main__:cli'
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