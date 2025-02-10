Getting Started
===============

Prerequisites
-------------
- Install Blender on your machine. Link: https://www.blender.org/download/
- Install the latest version of Python. Link: https://www.python.org/downloads/
- No programming knowledge is required to use this tool.

Setup
-----
- If you install Blender in a non-default path on Windows, note the path as it will be needed.
- Download the entire 'Gaussian-2-Blender' package and unzip it to the desired location.
- The executable ``Gaussian-2-Blender.exe`` will be ready to use. Do not move, rename, or delete any files or folders included in the package.
- Click on this `<https://youtu.be/w_bsJ7daaas>`_ for a tutorial on using the tool. NOTE: YouTube tutorial does not include information on animations.

Instructions
============

Example files
-------------
- Example ``.com`` and ``.xyz`` files are inside the ``input_examples`` folder, separated by categories.
- For example, the file ``Ice.com`` is located in the ``input_examples\com_files\inorganic\`` folder.
- The ``output`` folder starts empty and is the default location for 3D renderings from the tool.

Executing Gaussian-2-Blender
----------------------------
1. Double-click on the ``Gaussian-Blender-Bridge.exe`` file.
2. Select one or more ``.com`` or ``.xyz`` files from the same folder.
3. Select ``Is Animation`` to export as an animated ``fbx`` object
4. If you plan to render an animation, make sure all the ``.com`` or ``.xyz`` files have the exact same atoms in the exact same order
5. To render using ionic radii, select the ``Check for Ionic Radii`` option.
6. Add each ion and select their charge, coordination, and spin multiplicity (when available).
7. Click on ``Convert!`` to convert the ``.com`` or ``.xyz`` input into the desired output type.
8. Click on ``Reset`` to reset everything to their default values.

Running Gaussian-2-Blender from the console
-------------------------------------------
To run the ``Gaussian-2-Blender.py`` Python script from the console:
1. Copy the ``Gaussian-2-Blender.py`` file to the ``gui`` folder.
2. Open a terminal in the ``Blender-Gaussian-Bridge/`` folder and run:

.. code-block:: console

   $ python Gaussian-2-Blender.py
