from setuptools import setup

setup(
    name='dices',
    version='0.1',
    description='a simple game of dices',
    author='Frantisek Necas',
    author_email='fifinecas@seznam.cz',
    url='https://github.com/FrNecas/dices',
    license='MIT',
    packages=[
        'dices'
    ],
    entry_points={
        'console_scripts': [
            'dices = dices.application:main',    
        ],
    },
)
