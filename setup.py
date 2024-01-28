from setuptools import setup, find_packages
import pathlib

this_dir = pathlib.Path(__file__).parent.resolve()
readme = (this_dir / 'README.md').read_text(encoding='utf-8')

setup(
    name='trackyournet',
    version='1.0',
    description='A simple command-line app that runs a internet speedtest in a determined interval of time',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    license_files=['LICENSE.txt'],
    url='https://github.com/VictorioMaculan/internet-speed-tracker',
    author='Victorio H. S. Maculan',
    keywords='speedtest, speed test, internet speed, cli',
    package_dir={'': 'scr'},
    packages=find_packages(where='scr'),
    python_requires='>=3.7',
    install_requires=['pandas', 'schedule', 'speedtest-cli'],
    entry_points={
        'console_scripts': [
            'trackyournet = trackyournet:command_line_runner',
        ]
    },
    project_urls={
        'Bug Reports or Suggestions': 'https://github.com/VictorioMaculan/internet-speed-tracker/issues',
    }    
)
