from setuptools import setup, find_packages

packages = find_packages(exclude=['example', 'example.*'])

setup(
    name='duckadmin',
    version='0.1.2',
    license='BSD',
    discription='A Django reusable app for show and operate custom forms in admin.',
    author='Wang Chao',
    author_email='yueyoum@gmail.com',
    url='https://github.com/yueyoum/duckadmin',
    keywords='django, admin',
    packages=packages,
    package_data = {
        'duckadmin': ['templates/*.html']
    },
    install_requires = ['six']
)
