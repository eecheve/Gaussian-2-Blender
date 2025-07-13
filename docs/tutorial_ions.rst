.. _tutorial_ions:

5. TheorChem2Blender - Specifying ionic radii
==============================================

Overview
---------
TheorChem2Blender is a program that has 5 tabs. Which tabs to modify depend on the type of 3D file the user wants to create. For the simplest use of the program, you only need to specify the input, and convert it as output. The default output format is `glb`.
Below is a continuation on how to use **TheorChem2Blender**, focused specifying ionic radii information. Refer to :ref:`(3) basic use <tutorial_basic_use>` for information about how to choose `com` input files to convert, and :ref:`(4) highlighting bonds <tutorial_customization>` for how to highlight atoms and bonds.


Input tab
----------
1. Leave `.com` as the input file
2. Click on `set` to select the input name
3. Go to `inpuut_examples/com_files/minerals/`
4. Select `halite.com` as the input

Ions tab
---------
1. Select the `check for ionic radii` box

.. image:: /_static/images/tutorial5_step1.png
    :alt: Highlighting an atom or bond, step 1
    :width: 500px

2. Click on `add` to add an element

.. image:: /_static/images/tutorial5_step2.png
    :alt: Selecting .com input, step 4
    :width: 500px

3. Click on `Element` to select an element

.. image:: /_static/images/tutorial5_step3.png
    :alt: Selecting .com input, step 5
    :width: 500px

4. Select `Na` from the drop down list that appeared

.. image:: /_static/images/tutorial5_step4.png
    :alt: Selecting .com input, step 5
    :width: 500px

5. Specify the charge and coordination for the atom (+1) and VI for halite

.. image:: /_static/images/tutorial5_step5.png
    :alt: Selecting .com input, step 5
    :width: 500px

6. Follow steps 4 and 5 for the chloride anion with a coordination ov VI as well.

.. image:: /_static/images/tutorial5_step6.png
    :alt: Selecting .com input, step 5
    :width: 500px

8. Click on the Convert! tab
9. Convert the input to the default `glb` output format
10. Your file will appear by default in the `output/` folder.

.. note::

   🎥 To see a video recording of this walkthrough, visit the following link:  
   `Watch on YouTube <https://youtu.be/elOb1yUuWVY>`_


:ref:`Previous: (4) highlight atoms and bonds <tutorial_customization>`
:ref:`Next: (6) Animations with com input <tutorial_animation_com>`


----

:doc:`← Back to Tutorials Home <tutorial>`