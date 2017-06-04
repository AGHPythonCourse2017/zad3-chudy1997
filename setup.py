from setuptools import setup

setup(name='song_singer',
      version='1.0',
      description='Project allowing checking if '
                  'sentence about posessness of song is true.',
      url='https://github.com/AGHPythonCourse2017/zad3-chudy1997',
      author='Karol Bartyzel',
      author_email='karolbartyzel308@gmail.com',
      license='Freeware',
      packages=['song_singer'],
      install_requires=[
          'requests',
          'bs4',
          'pytest',
      ],
      zip_safe=False)
