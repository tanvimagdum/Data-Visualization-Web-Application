from setuptools import setup, find_packages

setup(
    name='myapp',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'plotly'
    ],
    entry_points={
        'console_scripts': [
            'run_app=application:run_app'
        ]
    }
)