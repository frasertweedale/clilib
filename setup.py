import distutils.core
import sys

import clilib  # import version info

with open('README') as fh:
    long_description = fh.read()

distutils.core.setup(
    name='clilib',
    version=clilib.version,
    description='Evidence Based Scheduling program',
    author='Fraser Tweedale',
    author_email='frase@frase.id.au',
    url='https://gitorious.org/clilib',
    packages=['clilib'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: User Interfaces',
    ],
    long_description=long_description,
)
