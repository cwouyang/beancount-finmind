try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='beancount-finmind',
    version='0.1.0',
    description='bean-price source from FinMind',
    packages=['beancount_finmind'],
    license='MIT',
)