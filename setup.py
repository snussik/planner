from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='planner',
    version='0.1.0',    
    description='Package for getting list of dates',
    url='https://github.com/snussik/planner.git',
    author='snussik',
    author_email='snussik@snussik.com',
    package_dir={"":"src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='BSD 2-clause',
    packages=['planner'],
    install_requires=['python-dateutil'],

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",     
        'Programming Language :: Python :: 3.8',
    ],
)