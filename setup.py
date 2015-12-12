from setuptools import find_packages, setup

packages = find_packages(exclude=['example'])

setup(
    name='duckadmin',
    version='0.1.0',
    license='BSD',
    discription='A Django reusable app for show and operate custom forms in admin.',
    long_description=open('README.txt', 'r').read(),
    author='Wang Chao',
    author_email='yueyoum@gmail.com',
    url='https://github.com/yueyoum/duckadmin',
    keywords='django, admin',
    packages=packages,
)
