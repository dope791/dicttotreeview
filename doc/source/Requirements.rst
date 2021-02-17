Requirements
--------------------------

- `readthedocs`_ - theme:

   .. _readthedocs: https://github.com/readthedocs/sphinx_rtd_theme

   This theme provides a clear and pretty document.
   Feel free to choose another one.

   To install the package use:
   ``pip install sphinx-rtd-theme``

- `sphinxcontrib_plantuml`_:

   .. _sphinxcontrib_plantuml: https://pypi.org/project/sphinxcontrib-plantuml/

   This package enables you to compile *uml-code* with sphinx.  
   To start a *uml-section* use ``.. uml::``.
   The path to the PlantUML file may have to be specified (assuming that Java itself is already in the search path).
   You need to implement the path of your file (.jar) to the ``conf.py``-file.

   Example:
   ``plantuml = 'java -jar C:\\tools\\plantuml.1.2020.17.jar'``
   
   PlantUML requires ``Graphviz`` and an **environment variable** may have to be defined, pointing to the dot executable.

   Example:
   **PATH** -> ``C:\tools\Graphviz\bin``
   (dot.exe exists inside this folder)

   Download ``Graphviz`` from the official `website`_.
   
   .. _website: https://graphviz.org/download/ 

   To install the package use: 
   ``pip install sphinxcontrib-plantuml`` 

   Interesting link for creating diagrams in Sphinx:
   `diagram_in_sphinx`_

   .. _diagram_in_sphinx: https://build-me-the-docs-please.readthedocs.io/en/latest/Using_Sphinx/UsingGraphicsAndDiagramsInSphinx.html

- Visual Studio Code:

  Install these **extensions** for Visual Studio Code:

   ====================  ==========================  =================
   Extension             ID                             
   ====================  ==========================  =================
   ``reStructuredText``  lextudio.restructuredtext   *necessary*
   ``PlantUML``          jebbs.plantuml              *recommended*
   ``Git History``       donjayamanne.githistory     *recommended*
   ``GitLens``           eamodio.gitlens             *recommended*
   ``Git Graph``         mhutchie.git-graph          *recommended*
   ====================  ==========================  =================  

   With the **Extension ID** you may search directly for the right extension in the marketplace of VSCode

  
