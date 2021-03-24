import sphinx_rtd_theme
import sys, os
from datetime import datetime

sys.path.append('..')

exclude_patterns = ['_build']


# -- Project information -----------------------------------------------------

project = 'dicttotreeview'

copyright = 'Baumer Electric AG, egr,'
author = 'egr'
if '' != "": 
    version = ''
else:
    version = '1.3'
release = '1.3'

# -- General configuration ---------------------------------------------------

extensions = ["sphinx_rtd_theme",
 "sphinxcontrib.plantuml",
 "sphinx.ext.autodoc",
 "sphinx.ext.coverage",
 "sphinx.ext.viewcode",
 "recommonmark",
 "sphinxcontrib.needs",
 "sphinxcontrib.test_reports",
 "breathe"    
]

needs_services = {
    'github-issues': {},
    'github-prs': {},
    'github-commits': {},
}

now = datetime.now()

#Use plantUML
plantuml = 'java -jar "C:/Users/Elena Grammel/Desktop/dicttotreeview/doc/plantuml.jar"'
templates_path = ['../templates']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "source/images/BaumerLogo.png"
html_last_updated_fmt = f"{now.month:02d}/{now.day:02d}/{now.year} {now.hour+1}:{now.minute:02d}:{now.second:02d}"



# -- The name of the Pygments (syntax highlighting) style to use. ------------

pygments_style = "sphinx"