Pootle VCS
----------

Pootle VCS app


``vcs`` command
---------------

Get VCS info for all projects

.. code-block:: bash

   pootle vcs


``set_vcs`` subcommand
----------------------

Set the VCS for a project. Project must exist in Pootle.

.. code-block:: bash

   pootle vcs myproject set_vcs git git@github.com:translate/myprojrepo


``info`` subcommand
-------------------

Get the VCS info for a project. This is the default command - so ``info`` can
be ommitted.

.. code-block:: bash

   pootle vcs myproject info

or...

.. code-block:: bash

   pootle vcs myproject


``fetch_translations`` subcommand
---------------------------------

Pull the VCS repository, and create a store_vcs object for each repository file
that has been matched from the ``.pootle.ini`` configuration file.

.. code-block:: bash

   pootle vcs myproject fetch_translations


``status`` subcommand
---------------------

List the status of files in Pootle and VCS - specifically files that are:

- only in Pootle
- only in VCS
- updated in Pootle
- updated in VCS
- updated in both Pootle and VCS

.. code-block:: bash

   pootle vcs myproject status


``pull_translations`` subcommand
--------------------------------

Pull translations from VCS into Pootle:

- Create stores in Pootle where they dont exist already
- Update exisiting stores from VCS translation file

.. code-block:: bash

   pootle vcs myproject pull_translations



---------------------------------------------

Proposed/unimplemented
^^^^^^^^^^^^^^^^^^^^^^


``add_translation`` subcommand
------------------------------

Add a translation from Pootle into VCS



``commit_translations`` subcommand
----------------------------------

Commit and push translations from Pootle into VCS



