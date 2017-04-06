from setuptools import setup, find_packages

setup(
    name='esc_identifier',
    version='',
    packages=find_packages(),
    author='Sergey Demurin',
    author_email='kakty3.mail@gmail.com',
    install_requires=[
        'biopython>=1.68',
        'psycopg2>=2.7.1',
        'sqlalchemy>=1.1.6',
        'sqlalchemy_utils>=0.32.13',
    ]
)
