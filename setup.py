from setuptools import setup

requirements = [
]


setup(
    name='api-farms',
    version=0.1,
    description="Simple API In Python ",
    author="Neil Seward",
    author_email='neil.seward@scotiabank.com',
    url='https://bitbucket.agile.bns/projects/AMLREPO/repos/api-farms',
    packages=['farm'],
    install_requires=requirements,
    keywords='api-farms',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
