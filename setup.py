from setuptools import setup, find_packages
from os.path import basename, splitext
from glob import glob

tests_requires = [
    "pytest==7.1.2",
    "pytest-mock==3.8.2"
]

install_requires = open("requirements.txt").read().splitlines()

packages = find_packages("src")

setup_requires = [
    "pytest-runner"
]

console_scripts = [
    'make_json=make_json.call:main',
]

setup(
    name='make_json',
    version='0.1.0',
    packages=packages,
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_requires=tests_requires,
    entry_points={'console_scripts': console_scripts}
)