from setuptools import setup, find_packages

with open('./README.md', encoding='UTF-8') as file:
    long_description = file.read()

setup(
    name='RelayController',
    version='0.1.0',
    python_requires=">=3.9",
    description='Relay controller service based on FastAPI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rob W3LGA',
    author_email='RobW3LGA@github.com',
    install_requires=[
        'fastapi',
        'first',
        'httpx',
        'simplepam',
        'uvicorn'
    ]
)