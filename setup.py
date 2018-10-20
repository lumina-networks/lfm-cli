import setuptools


setuptools.setup(
    zip_safe=True,
    name='lfmcli',
    version='2.0.0',
    url="https://github.com/luminanetworks/lfm-cli",
    author='Lumina Networks',
    author_email='oss-dev@luminanetworks.com',
    packages=setuptools.find_packages(),
    description='CLI and Python Binding Library for Lumina Flow Manager',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='LICENSE',
    install_requires=['click', 'requests', 'topology-yaml==0.1.1'],
    entry_points='''
        [console_scripts]
        lfm=lfmcli.cli:cli
    ''',

)
