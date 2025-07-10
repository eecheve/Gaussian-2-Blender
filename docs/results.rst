Visualizing Results
===================
After converting input into 3D modeling files, a variety of programs can be used to observe them.
**TheorChem2Blender** is designed with Blender in mind as the program to open the files, however,
the output types can be seen and modified from a variety of programs, including Unity, Maya, Unreal Engine, and others.

Please see the adequate documentation for using the aforementioned programs. For users interested only in converting
computational chemistry output into 3D renderings and observing them easily, use one of the two options below.

3D Viewer (Windows)
--------------------
- :ref:`Download <https://apps.microsoft.com/detail/9nblggh42ths?hl=en-US&gl=US>` 3D Viewer from the Microsoft store app.
- Open the output from **TheorChem2Blender** using 3D Viewer.

F3D (MacOS)
------------
- If you don't have it, first install :ref:`Homebrew <https://docs.brew.sh/Installation>`
- Then type the line
    .. code-block:: bash

     brew install f3d
- Open the output using F3D


.. note::
	**TheorChem2Blender** can produce *.fbx* files as one of the options. 
   A security vulnerability has been identified in the FBX file format, which could potentially lead to remote code execution. 
   This has led to **3D Viewer** disabling FBX file support in various applications to mitigate the risk.
   See more information :ref:`here <https://support.microsoft.com/en-us/windows/support-for-fbx-files-has-been-turned-off-in-3d-viewer-b7483e83-422c-4d65-b94d-853eb65cb134>`