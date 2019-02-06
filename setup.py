from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name='vkfriends-finder-server',
    version='0.2',
    packages=find_packages(),
    url='https://bitbucket.org/Delisa-sama/vkfriends-finder-server/src/master/',
    license='GPL',
    author='Delisa',
    author_email='delisa.sama@gmail.com',
    description='Server part of VK Friends/Post finder/analyzer.',
    install_requires=requirements
)
