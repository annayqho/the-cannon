from setuptools import setup

setup(name='TheCannon',
        version='0.3.5',
        description='Data-driven stellar parameters and abundances from spectra',
        url='http://github.com/annayqho/TheCannon',
        author='Anna Y. Q. Ho',
        author_email='annayqho@gmail.com',
        license='MIT',
        packages=[
            'TheCannon', 'TheCannon.helpers', 'TheCannon.helpers.triangle',
            'TheCannon.example_DR10', 'TheCannon.example_DR10.Data'],
        )

