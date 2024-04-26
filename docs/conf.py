# -- Path setup --------------------------------------------------------------
from os.path import abspath, dirname
here = abspath(dirname(__file__))
# -- Project information -----------------------------------------------------
project = 'TylerD'
copyright = '2024, gUTOnET'
author = 'Gustavo Maia Neto (Guto Maia)'
from tylerd import __version__
release = __version__
# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.ifconfig',
    'sphinxcontrib.plantuml',
]
plantuml = f'java -jar {here}/plantuml.jar'
html_static_path = ['_static']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'analytics_id': 'UA-32666248-1',
}
