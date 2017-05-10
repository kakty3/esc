from setuptools import setup, find_packages

setup(
    name='esc_identifier',
    version='0.0.1',
    packages=find_packages(),
    author='Sergey Demurin',
    author_email='kakty3.mail@gmail.com',
    install_requires=[
        'biopython>=1.68',
        'jellyfish>=0.5.6',
        'fuzzywuzzy>=0.15.0',
        'ngram>=3.3',
        'names>=0.3.0',
        'nltk>=3.2.2',
        'numpy>=1.12.1',
        'pandas>=0.20.1',
        'pymongo>=3.4.0',
        'psycopg2>=2.7.1',
        'python-Levenshtein>=0.12.0',
        'scipy>=0.19.0',
        'sklearn',
        'sqlalchemy>=1.1.6',
        'sqlalchemy_utils>=0.32.13',
    ],
    setup_requires=[
        'numpy>=1.12.1',
    ]
)
