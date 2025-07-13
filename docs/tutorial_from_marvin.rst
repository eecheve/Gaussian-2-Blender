.. _tutorial_from_marvin:

1. From MarvinSketch to Blender
================================

This tutorial guides you through the process of converting a molecule drawn in MarvinSketch into a format usable in Blender, using Open Babel and Gaussian2Blender.

Requisites
----------

Before starting, make sure you have the following installed:

- **Open Babel**  
  A chemical toolbox designed to speak the many languages of chemical data.  
  Documentation: `Open Babel 3.1.1 <https://openbabel.org/docs/dev/>`_

- **First Generation Marvin Software**  
  Includes MarvinSketch and MarvinView.

Step 1: Open MarvinView
-----------------------

1. Launch **MarvinView**.
2. Navigate to **Edit > Structure** to open a MarvinSketch window.
3. In the MarvinSketch window:
   - Draw your molecule.
   - Go to **Structure > Add > Explicit H Atoms** to add all hydrogen atoms.
   - Go to **Structure > Clean3D > Clean in 3D** to generate 3D coordinates.
4. Copy the molecule:
   - Go to **Edit > Copy As …**
   - Select **.mol** format.

Step 2: Convert to .mol2 with Open Babel
----------------------------------------

1. Open **Open Babel**.
2. Use the GUI or command line to convert the `.mol` file to `.mol2` format.

   Example command:

   .. code-block:: bash

      obabel input.mol -O output.mol2

Step 3: Use TheorChem2Blender
------------------------------

1. Open **TheorChem2Blender**.
2. Follow the tool's procedure to convert the `.mol2` file into the desired format for Blender (e.g., `.obj`, `.fbx`, etc.).
NOTE: For more information on the steps for using TheorChem2Blender, see tutorials 3 through 10 in this page.


:ref:`Next: (2) From Molecular Dynamics to Blender (General) <tutorial_from_md>`


----

:doc:`← Back to Tutorials Home <tutorial>`