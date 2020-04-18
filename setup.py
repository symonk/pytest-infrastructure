from setuptools import setup, find_packages

install_requires = ["colorama"]

with open("README.md") as f:
    long_description = f.read()
setup(
    name="pytest-infrastructure",
    description="pytest stack validation prior to testing executing",
    license="Apache Software License 2.0",
    author="Simon Kerr",
    url="https://github.com/symonk/pytest-infrastructure",
    version="0.0.1",
    author_email="jackofspaces@gmail.com",
    maintainer="Simon Kerr",
    maintainer_email="jackofspaces@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"pytest11": ["infrastructure = infrastructure.plugin"]},
    install_requires=install_requires,
    setup_requires=["setuptools_scm"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
    ],
)
