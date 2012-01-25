import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''
    
def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''

# Use the docstring of the __init__ file to be the description
DESC = " ".join(__import__('myshare').__doc__.splitlines()).strip()

setup(
    name = "Python Social Share",
    version = __import__('socialshare').get_version().replace(' ', '-'),
    url = 'http://directemployersfoundation.org/products/py-social-share',
    author = 'Mike Seidle',
    author_email = 'mike@directemployersfoundation.org',
    description = DESC,
    long_description = get_readme(),
    packages = find_packages(),
    include_package_data = True,
    install_requires = read_file('requirements.txt'),
    classifiers = [
        'License :: OSI Approved :: MIT License',
    ],
)
