from setuptools import setup, find_namespace_packages

setup(
    name='pydnd',
    version='0.1.1',
    description='Flexible Dungeons and Dragons entity manager and helper',
    author='Jesse McGaha',
    url='https://github.com/jrmcgaha-dev/pydnd',
    packages=find_namespace_packages(),
    python_requires='>=3.8',
    package_data={
        'pydnd': ['cr_to_xp.json']
    },
    entry_points={
        'console_scripts': [
            'pydnd = pydnd._main:main'
        ]
    }
)
