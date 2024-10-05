from setuptools import setup, find_packages


# Function to read requirements from requirements.txt
def read_requirements(filename):
    with open(filename, 'r') as file:
        # Return a list of requirements, stripping whitespace and comments
        return [line.strip() for line in file if line and not line.startswith('#')]


setup(
    name='agenticrag',
    version='0.1',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'onboard_pdf=agenticrag.process_pdf:main',
            'start_rag_app=agenticrag.start_app:main'
        ],
    },
)
