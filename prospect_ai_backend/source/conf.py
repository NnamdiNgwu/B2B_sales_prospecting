# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ProspectAI Navigator'
copyright = '2025, Nnamdi Ngwu'
author = 'Nnamdi Ngwu'
release = '2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Core library to pull documentation from docstrings
    'sphinx.ext.napoleon', # Support for Google-style docstrings
    'sphinx.ext.viewcode', # Add links to source code
    'myst_parser',        # Add Markdown parser
    'sphinx_mermaid',     # Add Mermaid diagram support
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


# -- Path setup --------------------------------------------------------------
# This is the crucial part that allows Sphinx to find your Python files.
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))