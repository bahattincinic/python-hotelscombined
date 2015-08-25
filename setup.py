from setuptools import setup, find_packages

setup(
    name='python-hotelscombined',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/metglobal/python-hotelscombined',
    license='MIT',
    author='Metglobal',
    author_email='bahattincinic@gmail.com',
    description='Python Client For Hotels Combined',
    install_requires=['requests'],
    tests_require=['httpretty'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
