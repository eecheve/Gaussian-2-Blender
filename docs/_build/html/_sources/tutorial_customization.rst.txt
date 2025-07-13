.. _tutorial_customization:

4. TheorChem2Blender - Highlighting atoms and bonds
====================================================

Overview
---------
TheorChem2Blender is a program that has 5 tabs. Which tabs to modify depend on the type of 3D file the user wants to create. For the simplest use of the program, you only need to specify the input, and convert it as output. The default output format is `glb`.
Below is a continuation on how to use **TheorChem2Blender**, focused on highlighting atoms and bonds. Refer to :ref:`(3) basic use <tutorial_basic_use>` for information about how to choose `com` input files to convert.


Input tab
----------
1. Leave `.com` as the input file
2. Click on `set` to select the input name
3. Go to `inpuut_examples/com_files/organic/`
4. Select `E-2-fluorovinyloxytrimethylsilane.com` as the input

Customization tab
------------------
1. Check the `highlight atoms` box to allow user input

.. image:: /_static/images/tutorial4_step1.png
    :alt: Highlighting an atom or bond, step 1
    :width: 500px

2. For this example type the following in the `Atom list` box:

.. code-block::

    C02, C03

3. Check the `highlight bonds` box to allow user input

.. image:: /_static/images/tutorial4_step2.png
    :alt: Selecting .com input, step 4
    :width: 500px

4. To highlight bonds, specify the character that represents a given bond order.
   For this example, type the following in the `Bonds list` box:

.. code-block::

    C02=C03

.. image:: /_static/images/tutorial4_step3.png
    :alt: Selecting .com input, step 5
    :width: 500px

5. Click on the `Convert!` tab. Convert the input afterwards.
6. Your file will appear by default in the `output/` folder.

.. note::

   🎥 To see a video recording of this walkthrough, visit the following link:  
   `Watch on YouTube <https://youtu.be/oi2I2vRrcLw>`_


:ref:`Previous: (3) Basic use <tutorial_basic_use>`
:ref:`Next: (5) For ionic compounds <tutorial_ions>`

----

:doc:`← Back to Tutorials Home <tutorial>`