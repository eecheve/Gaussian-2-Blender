Getting Started
===============

Prerequisites
-------------
- Install Blender on your machine. Link: https://www.blender.org/download/
- Install the latest version of Python. Link: https://www.python.org/downloads/
- No programming knowledge is required to use this tool.

.. note::
    **TheorChem2Blender** *V.2025.2* was built for **Blender** *V.4.2*. If you encounter unexpected
    running errors, please check your version of Blender and download the appropriate one.

Setup
-----
- If you install Blender in a non-default path on Windows, note the path as it will be needed.
- Download the entire 'TheorChem2Blender' package and unzip it to the desired location.
- Do not move, rename, or delete any files or folders included in the package.
- Click on this `<https://youtu.be/w_bsJ7daaas>`_ for a tutorial on using the tool. NOTE: YouTube tutorial does not include information on animations.

Instructions
============

Running the Executable from Windows
-----------------------------------
1. Double-click on the ``TheorChem2Blender_Windows.exe`` file.
2. Select one or more ``.com``, ``.xyz``, ``.mol2`` files from the same folder.
3. Select ``Is Animation`` to export as an animated ``fbx`` object.
4. If you plan to render an animation, make sure all the ``.com`` or ``.xyz`` files have the exact same atoms in the exact same order.
5. To render using ionic radii, select the ``Check for Ionic Radii`` option.
6. Add each ion and select their charge, coordination, and spin multiplicity (when available).
7. Click on ``Convert!`` to convert the ``.com`` or ``.xyz`` input into the desired output type.
8. Click on ``Reset`` to reset everything to their default values.

Running the Executable from macOS
---------------------------------
1. Navigate to the ``macOS`` folder inside the unzipped Chem2Blender package.
2. Double-click on the ``TheorChem2Blender.app`` executable.
3. Follow the same steps as in the Windows section to select files, configure options, and convert.

Running Chem2Blender from the Console
-------------------------------------
To run the ``TheorChem2Blender.py`` Python script from the console:
1. Copy the ``TheorChem2Blender.py`` file to the ``gui`` folder.
2. Open a terminal in the ``Blender-Gaussian-Bridge/`` folder and run:

.. code-block:: console

   $ python TheorChem2Blender.py

Example Files
-------------
- Example ``.com`` and ``.xyz`` files are inside the ``input_examples`` folder, separated by categories.
- For example, the file ``Ice.com`` is located in the ``input_examples\\com_files\\inorganic\\`` folder.
- The ``output`` folder starts empty and is the default location for 3D renderings from the tool.