from setuptools import setup


install_requires = open('requirements.txt').read().split('\n')


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
        name='detimotic',
        version='0.1',
        description='API for the demitotic platform',
        long_description = long_description,
        long_description_content_type="text/markdown",
        url='',
        author='Catarina Silva',
        author_email='c.alexandracorreia@ua.pt',
        license='MIT',
        install_requires=install_requires,
        packages=['detimotic']
)
