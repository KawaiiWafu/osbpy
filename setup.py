from setuptools import setup
import os.path

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
]

setup(
    name="osbpy",
    version="2.1.0",
    packages=['osbpy'],
    include_package_data=True,
    install_requires=[
        'matplotlib>=2.1.0',
        'numpy>=1.13.3+mkl',
        'scipy>=1.0.0'
    ],
    author="Jiri Olszar",
    author_email="remiliass@gmail.com",
    description="Simple library for osu! storyboarding",
    long_description=open(
        os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    classifiers=classifiers,
    license="MIT",
    keywords="graphics audio rhythm game",
    url="https://github.com/KawaiiWafu/osbpy",
    python_requires=">=3",
)
