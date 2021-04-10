***************
dicttotreeview
***************

.. |python| image:: https://img.shields.io/badge/python-3.7-blue
  :target: https://www.python.org/dev/peps/pep-0537/
.. |docs| image:: https://img.shields.io/badge/docs-master-orange
  :target: file:///C:/Users/Elena%20Grammel/Desktop/dicttotreeview/doc/_build/html/index.html
.. |version| image:: https://img.shields.io/badge/version-1.4-green
  :target: https://github.com/dope791/dicttotreeview/releases/tag/1.4


|python| |docs| |version|


This package displays and actualizes a given dictionary on a given TreeView. (GUI)
Customizable features for filtering dicts and displaying lists.      
This package inherits from ``QStandardItemModel`` and other.


Web resources
=============


* **GitHub Repository**: https://github.com/dope791/dicttotreeview 


* **Documentation**: file:///C:/Users/Elena%20Grammel/Desktop/dicttotreeview/doc/_build/html/index.html
   

Usage
=====


**Initialization:**

.. code:: python

    from dicttotreeview import DictToTreeView

    DictToTreeView(data_dict, TreeView)



Installation
============

pip
---

If you use ``pip``, you can install ``DictToTreeView`` from our `PO1 Package Registry`_ with:

.. code:: bash

    pip install dicttotreeview

If you cannot install packages from our `PO1 Package Registry`_ please reade the guide on how to configure your ``pip.ini`` file.

.. _PO1 Package Registry: https://gitlab.baumernet.org/bech/rd/po1/package-registry

Git+SSH
-------

If you have access to the repository, you can also install a specific **<tag>** with: 

.. code:: bash

    python -m pip install --upgrade "git+ssh://github.com/dope791/dicttotreeview.git@<tag>"








