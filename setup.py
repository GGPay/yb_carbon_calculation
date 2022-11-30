import setuptools
from setuptools import find_packages

__description__ = "YB Carbon Calculation"
__repo_name__ = "yb_carbon_calculation"
__folder_that_has_code_ = "yb_carbon_calculation"


with open("./requirements.txt", "r") as req_file:
    REQUIREMENTS = req_file.read().splitlines()


setuptools.setup(
    name='yb_carbon_calculation',
    version='0.0.1',
    description=__description__,
    author='YB Data Engineering Team',
    author_email='data-engineering@yb.com',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires='>=3.9',
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=REQUIREMENTS,
    package_data={"": ["*"]},
    entry_points={
        'console_scripts': [
            "yb_carbon_calculation = yb_carbon_calculation.main:run_carbon_analytics",
        ],
    },

)
