.. _tutorial_unit_cell:

8. TheorChem2Blender - Unit cells, growth, Miller planes, and polyhedra
=========================================================================

Overview
---------
TheorChem2Blender is a program that has 6 tabs: Input, Customization, Ions, Unit Cells, Output, and Convert!. Which tabs to modify depend on the type of 3D file the user wants to create. The `Unit Cells` tab is different from the others covered so far - it only becomes available when the input file type is `.vasp`, since periodic cell information is read from VASP-format files.
Below is a continuation on how to use **TheorChem2Blender**, focused on rendering unit cell boundaries, growing supercells, drawing crystallographic (Miller) planes, and building coordination polyhedra from a `.vasp` input. Refer to :ref:`(3) basic use <tutorial_basic_use>` for the general input/convert workflow.


Input tab
----------
1. Change the input type to `.vasp`
2. Click on `set` to select the input name
3. Go to `input_examples/vasp_files/`
4. Select `SrTiO3_perovskite.vasp` as the input
5. Notice the `Unit Cells` tab, previously greyed out, is now available - this only happens for `.vasp` input
6. Go to the `Unit Cells` tab

Unit Cells tab
---------------
7. If you defined cell boundaries in the `.vasp` file using a bond order of 0.5, check `unit cell boundaries` to render them as solid unit cell edges instead of dashed lines

8. Check `allow unit cell growth` to render one or more duplicated copies of the unit cell
9. Click `add cell growth`, then choose how many times to repeat the cell along `x`, `y`, and `z` - for this example, try `2, 2, 2`

.. code-block::

    x: 2  y: 2  z: 2

10. Click `add cell growth` again if you want to render more than one growth size in the same batch - for example, also add `1, 1, 1` to keep the original cell alongside the 2x2x2 supercell

11. Check `allow Miller indices` to render crystallographic planes
12. Click `add plane`, then choose `h`, `k`, and `l` - for this example, try `1, 0, 0`

.. code-block::

    h: 1  k: 0  l: 0

13. Click `add plane` again for more planes, e.g. `1, 1, 1`. Every plane you add is rendered on every unit cell growth size defined in steps 9-10

14. Check `build polyhedra` to draw coordination polyhedra around selected center atoms
15. Click `add center`, then choose the element that will act as the polyhedron center - for this example, choose `Ti`, so a polyhedron is drawn around every titanium atom with three or more bonded oxygen neighbors
16. Click `add center` again to build polyhedra around a second element type, if desired

17. Click `Clear` at any point to reset unit cell boundaries, growth, Miller planes, and polyhedra back to empty
18. Go to the `Convert!` tab

Convert! tab
-------------
19. Click on `Convert!`
20. If you added more than one unit cell growth size, one output file is generated per growth size, each with every Miller plane rendered on it
21. Your file(s) will appear by default in the `output/` folder

.. note::

   🎥 To see a video recording of this walkthrough, visit the following link:
   [video coming soon]


:ref:`Previous: (7) animating xyz files <tutorial_animation_xyz>`


----

:doc:`← Back to Tutorials Home <tutorial>`
