from setuptools import setup


setup(
    name='django-autoclean',
    version='0.0.1',
    description='A Django model field that eases the get_or_create method to check duplicates',
    author='Aamir Adnan',
    author_email='s33k.n.d3str0y@gmail.com',
    url='https://github.com/intellisense/django-autoclean',
    license='MIT',
    packages=['autoclean', ],
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
    install_requires=[
        'Django>=1.4.3'
    ],
)
