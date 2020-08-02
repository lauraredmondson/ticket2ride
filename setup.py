from setuptools import setup

setup(name='ticket2ride',
      version='0.1',
      description='ticket2ride: generate fan ticket2ride map',
      url='https://github.com/lauraredmondson/ticket2ride
      author='Laura Edmondson',
      author_email='lredmondsonl@sheffield.ac.uk',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
      ],
      packages=['ticket2ride'],
      install_requires=[
          'numpy','pandas','matplotlib','networkx'
      ],
      zip_safe=False,
      )
