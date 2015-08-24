from setuptools import setup, find_packages

setup(
    name='python-hotelscombined',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/bahattincinic/python-hotelscombined',
    license='MIT',
    author='Bahattin Cinic',
    author_email='bahattincinic@gmail.com',
    description='Python Client For Hotels Combined',
    install_requires=['requests'],
)
