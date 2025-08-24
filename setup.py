from setuptools import setup, find_packages

setup(
    name="aqvh-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.36.0",
        "numpy>=1.26.4",
        "pandas>=2.2.2",
    ],
    python_requires=">=3.8",
)