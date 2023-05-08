from setuptools import setup

__version__ = "0.4.1"

def load_requirements(filename):
    with open(filename, "rt") as fh:
        return fh.read().rstrip().split("\n")

with open("README.md") as f:
    long_description = f.read()

setup(
    name="markdown-to-respec",
    version=__version__,
    author="Ed Summers",
    author_email="info@webrecorder.net",
    license="Apache 2.0",
    py_modules=["markdown_to_respec"],
    url="https://github.com/webrecorder/markdown-to-respec",
    description="Convert specifications written in Markdown to ReSpec HTML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=load_requirements("requirements.txt"),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "markdown-to-respec = markdown_to_respec:main"
        ]
    }
)
