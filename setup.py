from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
long_description = f.read()


setup(name='MyNQL',
      version='0.1',
      description='My Network Query Language',
      long_description=long_description, 
      author='Florian Scholz',
      author_email='livint@posteo.de',
      url='https://www.github.com/livinter/MyNQL/',
      packages=['MyNQL', 'distutils.command'],
       classifiers=[
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Recomendation Database',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='recomendation query languange', 
      install_requires=['networkx','yaml'],
     )

