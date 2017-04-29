from setuptools import setup, find_packages

setup(
    name='esc_identifier',
    version='0.0.1',
    packages=find_packages(),
    author='Sergey Demurin',
    author_email='kakty3.mail@gmail.com',
    install_requires=[
        'biopython>=1.68',
        'fuzzywuzzy>=0.15.0',
        'numpy>=1.12.1',
        'psycopg2>=2.7.1',
        'python-Levenshtein>=0.12.0',
        'redis>=2.10.5',
        'scipy>=0.19.0',
        'sklearn',
        'sqlalchemy>=1.1.6',
        'sqlalchemy_utils>=0.32.13',
    ],
    setup_requires=[
        'numpy>=1.12.1',
    ]
)
