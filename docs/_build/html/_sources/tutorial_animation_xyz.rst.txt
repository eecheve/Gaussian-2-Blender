.. _tutorial_animation_xyz:

7. TheorChem2Blender - Animating .xyz input
==============================================

Overview
---------
TheorChem2Blender is a program that has 5 tabs. Which tabs to modify depend on the type of 3D file the user wants to create. For the simplest use of the program, you only need to specify the input, and convert it as output. The default output format is `glb`.
Below is a continuation on how to use **TheorChem2Blender**, focused animating `.com` input. Refer to :ref:`(3) basic use <tutorial_basic_use>` for information about how to choose `com` input files to convert, :ref:`(4) highlighting bonds <tutorial_customization>` for how to highlight atoms and bonds, :ref:`(5) specifying ions <tutorial_ions>` for ionic compounds, and :ref:`(6) animating com files <tutorial_animation_com>` for animating com files.


Input tab
----------
1. Change the input to `.xyz`
2. Click on `set` to select the input name
3. Go to `inpuut_examples/xyz_files/trajectories/`
4. Select the `carbon_dioxide_symmetric_vibration.xyz` file
5. Select `is animation`
6. Go to the `Customization` tab

.. image:: /_static/images/tutorial7_step1.png
    :alt: Highlighting an atom or bond, step 1
    :width: 500px

Customization tab
------------------

7. Because for this example, the bond length of the input is larger than a C-O bond, click on `force bonds`

.. image:: /_static/images/tutorial7_step2.png
    :alt: Highlighting an atom or bond, step 1
    :width: 500px

8. Type the following on the `Forced bonds list` box: (If you type C01=O03 instead, the bond will be inverted)
   When forcing a bond, if the colors are inverted, try changing the order of the atoms as is this case.

.. code-block::

    C01=O02; O03=C01

.. image:: /_static/images/tutorial7_step3.png
    :alt: Highlighting an atom or bond, step 1
    :width: 500px

9. Click on the `Output` tab

Output tab
-----------
10. Select `fbx` as the output format
11. Click on the `Convert!` tab

Convert! tab
-------------
9. Convert the input
10. Your file will appear by default in the `output/` folder.

.. note::

   🎥 To see a video recording of this walkthrough, visit the following link:  
   `Watch on YouTube <https://youtu.be/V0ARxJZNfy8>`_

   🎥 To see a video recording of of another animation, customizing and highlighting bonds, visit this link:  
   `Watch on YouTube <https://youtu.be/Ee8SqCKStUw>`_


:ref:`Previous: (6) animating com files <tutorial_animation_com>`


----

:doc:`← Back to Tutorials Home <tutorial>`