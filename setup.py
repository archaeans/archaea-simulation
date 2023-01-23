from distutils.core import setup

setup(
    name='archaea-simulation',
    packages=['archaea_simulation.simulation_objects'],
    version='1.0.0',
    license='Apache 2.0',
    description='Wrapper definitions for simulation tools.',
    readme='README.md',
    author='Oğuzhan Koral',
    author_email='oguzhankoral@gmail.com',
    url='https://github.com/archaeans/archaea-simulation',
    download_url='https://github.com/archaeans/archaea-simulation/archive/refs/tags/1.0.0.tar.gz',
    keywords=['geometry', 'simulation'],
    install_requires=[
        'archaea'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
)
