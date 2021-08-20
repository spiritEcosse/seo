import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


# Get the version
from seo import __version__


def get_long_description():
    readme = ""

    with open('README.md', encoding='utf-8') as readme_file:
        readme = readme_file.read()

    return readme


REQUIREMENTS_FOLDER = os.getenv('REQUIREMENTS_PATH', '')
requirements = [line.strip() for line in open(os.path.join(REQUIREMENTS_FOLDER, "requirements.txt"), 'r')]
test_requirements = [line.strip() for line in open(os.path.join(REQUIREMENTS_FOLDER, "requirements_dev.txt"), 'r')]


setup(
    name='seo',
    version='{version}'.format(version=__version__),
    description="Seo microservice for work seo information of pages on frontend",
    long_description=get_long_description(),
    author="seo",
    author_email='me@aalhour.com',
    url='seo/api/v1.0/',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "seo": [
            "docs/*",
            "templates/*",
            "static/*",
            "static/js/*",
            "static/css/*",
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords="seo",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'run_seo=seo.app:run_app',
            'init_example=seo.init_example:init_example'
        ]
    }
)
