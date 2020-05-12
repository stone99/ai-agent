#!/usr/bin/env python
from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = ""

packages = [
    "serpent",
    "serpent.game_agents",
    "serpent.game_launchers",
    "serpent.games",
    "serpent.input_controllers",
    "serpent.machine_learning",
    "serpent.machine_learning.context_classification",
    "serpent.machine_learning.context_classification.context_classifiers",
    "serpent.machine_learning.reinforcement_learning",
    "serpent.visual_debugger",
    "serpent.wamp_components",
    "serpent.window_controllers"
]

data_files = [
    ("serpent/templates/SerpentGameAgentPlugin", [
        "serpent/templates/SerpentGameAgentPlugin/plugin.py",
        "serpent/templates/SerpentGameAgentPlugin/__init__.py",
        "serpent/templates/SerpentGameAgentPlugin/.gitignore",
        "serpent/templates/SerpentGameAgentPlugin/.gitattributes"
    ]),
    ("serpent/templates/SerpentGameAgentPlugin/files", [
        "serpent/templates/SerpentGameAgentPlugin/files/serpent_game_agent.py",
        "serpent/templates/SerpentGameAgentPlugin/files/__init__.py"
    ]),
    ("serpent/templates/SerpentGameAgentPlugin/files/ml_models", [
        "serpent/templates/SerpentGameAgentPlugin/files/ml_models/.gitkeep"
    ]),
    ("serpent/templates/SerpentGameAgentPlugin/files/helpers", [
        "serpent/templates/SerpentGameAgentPlugin/files/helpers/.gitkeep"
    ]),
    ("serpent/templates/SerpentGamePlugin", [
        "serpent/templates/SerpentGamePlugin/plugin.py",
        "serpent/templates/SerpentGamePlugin/__init__.py",
        "serpent/templates/SerpentGamePlugin/.gitignore"
    ]),
    ("serpent/templates/SerpentGamePlugin/files", [
        "serpent/templates/SerpentGamePlugin/files/serpent_game.py",
        "serpent/templates/SerpentGamePlugin/files/__init__.py"
    ]),
    ("serpent/templates/SerpentGamePlugin/files/data/sprites", [
        "serpent/templates/SerpentGamePlugin/files/data/sprites/.gitkeep"
    ]),
    ("serpent/templates/SerpentGamePlugin/files/api", [
        "serpent/templates/SerpentGamePlugin/files/api/api.py",
        "serpent/templates/SerpentGamePlugin/files/api/__init__.py"
    ]),
    ("serpent/config", [
        "serpent/config/config.yml",
        "serpent/config/config.plugins.yml"
    ]),
    ("serpent", [
        "serpent/offshoot.manifest.json",
        "serpent/offshoot.yml",
        "serpent/requirements.linux.txt",
        "serpent/requirements.win32.txt",
        "serpent/requirements.darwin.txt"
    ])
]

requires = [
    "offshoot",
    "Cython==0.26.1"
]

setup(
    name='SerpentAI',
    version="2018.1.0",
    description='Game Agent Development Kit. Helping you create AIs / Bots to play any game you own!',
    long_description=long_description,
    author="Nicholas Brochu",
    author_email='nicholas@serpent.ai',
    packages=packages,
    data_files=data_files,
    include_package_data=True,
    install_requires=requires,
    entry_points={
        'console_scripts': ['serpent = serpent.serpent:execute']
    },
    license='MIT',
    url='https://github.com/SerpentAI/Serpent',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Games/Entertainment'
    ]
)
