UML Components Diagram
========================
This page presents two inheritance diagrams: one illustrating the Blender API structure and the other depicting the graphical user interface (GUI).

- The main script is highlighted in gray.
- The functions it calls are shown in light blue.
- The modules associated with each function are displayed in light green.

Blender API
------------------------

.. graphviz::

   digraph API {
       node [shape=box, style=filled];

       Main_Body [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];

       Obtain_Coords_Connect [fillcolor=lightblue];
       Manage_Ionic_Information [fillcolor=lightblue];
       Prepare_Atoms_and_Bonds [fillcolor=lightblue];
       Prepare_Ions [fillcolor=lightblue];
       Build_Molecule [fillcolor=lightblue];
       Highlight_Atoms [fillcolor=lightblue];
       Highlight_Bonds [fillcolor=lightblue];
       Animate [fillcolor=lightblue];
       Manage_Export [fillcolor=lightblue];
       Read_com_File [fillcolor=lightblue];
       Read_xyz_File [fillcolor=lightblue];

       Raw_Parameters [fillcolor=lightgreen];
       XyzReader [fillcolor=lightgreen];
       Refine_Data [fillcolor=lightgreen];
       Refine_Elements [fillcolor=lightgreen];
       Create_Materials [fillcolor=lightgreen];
       Ions [fillcolor=lightgreen];
       Instantiate_Molecules [fillcolor=lightgreen];
       AtomHighlighter [fillcolor=lightgreen];
       Animate_Module [fillcolor=lightgreen];
       Export_Data [fillcolor=lightgreen];

       Main_Body -> Obtain_Coords_Connect;
       Main_Body -> Manage_Ionic_Information;
       Main_Body -> Prepare_Atoms_and_Bonds;
       Main_Body -> Prepare_Ions;
       Main_Body -> Build_Molecule;
       Main_Body -> Highlight_Atoms;
       Main_Body -> Highlight_Bonds;
       Main_Body -> Animate;
       Main_Body -> Manage_Export;

       Obtain_Coords_Connect -> Read_com_File;
       Obtain_Coords_Connect -> Read_xyz_File;
       Read_com_File -> Raw_Parameters;
       Read_xyz_File -> XyzReader;

       Manage_Ionic_Information -> Refine_Data;

       Prepare_Atoms_and_Bonds -> Refine_Elements;
       Prepare_Atoms_and_Bonds -> Create_Materials;

       Prepare_Ions -> Refine_Elements;
       Prepare_Ions -> Ions;

       Build_Molecule -> Instantiate_Molecules;

       Highlight_Atoms -> AtomHighlighter;
       Highlight_Bonds -> AtomHighlighter;

       Animate -> Animate_Module;

       Manage_Export -> Animate_Module;
       Manage_Export -> Export_Data;
   }



GUI
----

.. graphviz::

   digraph Gaussian2Blender {
      node [shape=box, style=filled];

      Gaussian2Blender [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];

      assign_ionic_params [fillcolor=lightblue];
      convert [fillcolor=lightblue];
      convert_manager [fillcolor=lightblue];
      exceptions_test_passed [fillcolor=lightblue];
      help_animation_convert [fillcolor=lightblue];
      help_single_convert [fillcolor=lightblue];
      individual_convert [fillcolor=lightblue];
      initialize_animation_tutorial [fillcolor=lightblue];
      initialize_single_tutorial [fillcolor=lightblue];
      overwrite_animation_frames [fillcolor=lightblue];
      overwrite_parameters_script [fillcolor=lightblue];
      reset_to_defaults [fillcolor=lightblue];

      IonRegion [fillcolor=lightgreen];
      Tutorial [fillcolor=lightgreen];
      Utility [fillcolor=lightgreen];
      BlenderPath [fillcolor=lightgreen];
      OutputRegion [fillcolor=lightgreen];
      InputRegion [fillcolor=lightgreen];
      ConsoleRegion [fillcolor=lightgreen];
      Information [fillcolor=lightgreen];

      Gaussian2Blender -> assign_ionic_params;
      Gaussian2Blender -> convert;
      Gaussian2Blender -> convert_manager;
      Gaussian2Blender -> exceptions_test_passed;
      Gaussian2Blender -> help_animation_convert;
      Gaussian2Blender -> help_single_convert;
      Gaussian2Blender -> individual_convert;
      Gaussian2Blender -> initialize_animation_tutorial;
      Gaussian2Blender -> initialize_single_tutorial;
      Gaussian2Blender -> overwrite_animation_frames;
      Gaussian2Blender -> overwrite_parameters_script;
      Gaussian2Blender -> reset_to_defaults;

      assign_ionic_params -> IonRegion;

      convert -> convert_manager;

      convert_manager -> exceptions_test_passed;
      convert_manager -> assign_ionic_params;
      convert_manager -> individual_convert;

      exceptions_test_passed -> BlenderPath;
      exceptions_test_passed -> InputRegion;
      exceptions_test_passed -> IonRegion;

      help_animation_convert -> Tutorial;

      help_single_convert -> Tutorial;

      individual_convert -> overwrite_animation_frames;
      individual_convert -> overwrite_parameters_script;

      initialize_animation_tutorial -> InputRegion;
      initialize_animation_tutorial -> OutputRegion;
      initialize_animation_tutorial -> ActionRegion;

      initialize_single_tutorial -> InputRegion;
      initialize_single_tutorial -> OutputRegion;
      initialize_single_tutorial -> ActionRegion;

      overwrite_animation_frames -> Utility;

      overwrite_parameters_script -> Utility;

      reset_to_defaults -> BlenderPath;
      reset_to_defaults -> OutputRegion;
      reset_to_defaults -> InputRegion;
      reset_to_defaults -> IonRegion;
      reset_to_defaults -> ConsoleRegion;
      reset_to_defaults -> Information;
      reset_to_defaults -> Tutorial;

   }


