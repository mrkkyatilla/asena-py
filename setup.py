from setuptools import setup, find_packages

setup(
    name='music-analyzer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'librosa',
        'numpy',
        'soundfile',
        'tensorflow',
        'basic_pitch',
    ],
    author='Oser',
    description='Ses dosyasından enstrüman ve nota tanıma aracı',
    python_requires='>=3.8',
)
