from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="pytest-validate",
    use_scm_version={"write_to": "src/pytest_validate/_version.py"},
    author="Simon Kerr",
    version="0.0.1",
    author_email="jackofspaces@gmail.com",
    maintainer="Simon Kerr",
    maintainer_email="jackofspaces@gmail.com",
    license="Apache Software License 2.0",
    url="https://github.com/symonk/pytest-validate",
    description="pytest stack validation prior to testing executing",
    long_description=long_description,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers/QA",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={"pytest11": ["pytest_validate = pytest_validate.plugin"]},
)
