Program Architecture
========================
TheorChem2Blender is handled by two main python scripts that comunicate with each other by a OS-dependent executable script.
The API is handled by Main_Body.py, and the GUI by TheorChem2Blender.py. The two scripts are linked by either ReadMolecules.bat 
(Windows) or ReadMolecules.sh (MacOS). Below are three UML component diagrams illustrating the broad structure of the program.

- The main scripts are shown in gray.
- The principal functions called are shown in light blue.
- The modules associated with each function are displayed in light green.
- Data or parameter files are purple.

Program Outline
----------------

.. graphviz::

   digraph Outline {
         rankdir = LR;
         node [shape=box, style=filled];

         Main_Body [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];
         TheorChem2Blender [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];
         
         covalent_radii [fillcolor=lavender];
         ionic_radii [fillcolor=lavender];
         atomic_radii [fillcolor=lavender];

         t2b_config [fillcolor=lavender];

         ReadMolecules_bat [fillcolor=lightgreen];
         ReadMolecules_sh [fillcolor=lightgreen];

         if_windows [shape=box, style=filled, fillcolor=white, color=white];
         if_mac_os [shape=box, style=filled, fillcolor=white, color=white];

         covalent_radii -> TheorChem2Blender;
         
         TheorChem2Blender -> t2b_config;

         t2b_config -> if_windows;
         t2b_config -> if_mac_os;

         if_windows -> ReadMolecules_bat;
         if_mac_os -> ReadMolecules_sh;

         ReadMolecules_bat -> Main_Body;
         ReadMolecules_sh -> Main_Body;
         ionic_radii -> Main_Body;
         atomic_radii -> Main_Body;
   }



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
       Read_mol2_File [fillcolor=lightblue];

       Raw_Parameters [fillcolor=lightgreen];
       XyzReader [fillcolor=lightgreen];
       Mol2Reader [fillcolor=lightgreen];
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
       Obtain_Coords_Connect -> Read_mol2_File;
       Read_com_File -> Raw_Parameters;
       Read_xyz_File -> XyzReader;
       Read_mol2_File -> Mol2Reader;

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

   digraph GUI {
      node [shape=box, style=filled];

      TheorChem2Blender [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];

      assign_ionic_params [fillcolor=lightblue];
      convert [fillcolor=lightblue];
      convert_manager [fillcolor=lightblue];
      exceptions_test_passed [fillcolor=lightblue];
      individual_convert [fillcolor=lightblue];
      overwrite_animation_frames [fillcolor=lightblue];
      overwrite_parameters_script [fillcolor=lightblue];
      reset_to_defaults [fillcolor=lightblue];

      IonRegion [fillcolor=lightgreen];
      Utility [fillcolor=lightgreen];
      ActionsRegion [fillcolor=lightgreen];
      BlenderPath [fillcolor=lightgreen];
      OutputRegion [fillcolor=lightgreen];
      InputRegion [fillcolor=lightgreen];
      ConsoleRegion [fillcolor=lightgreen];
      Information [fillcolor=lightgreen];

      TheorChem2Blender -> assign_ionic_params;
      TheorChem2Blender -> convert;
      TheorChem2Blender -> convert_manager;
      TheorChem2Blender -> exceptions_test_passed;
      TheorChem2Blender -> individual_convert;
      TheorChem2Blender -> overwrite_animation_frames;
      TheorChem2Blender -> overwrite_parameters_script;

      assign_ionic_params -> IonRegion;

      convert -> ActionsRegion;
      reset_to_defaults -> ActionsRegion;
      individual_convert -> ActionsRegion;

      convert -> convert_manager;

      convert_manager -> exceptions_test_passed;
      convert_manager -> assign_ionic_params;
      convert_manager -> individual_convert;

      exceptions_test_passed -> BlenderPath;
      exceptions_test_passed -> InputRegion;
      exceptions_test_passed -> IonRegion;

      individual_convert -> overwrite_animation_frames;
      individual_convert -> overwrite_parameters_script;

      overwrite_animation_frames -> Utility;
      overwrite_parameters_script -> Utility;

      reset_to_defaults -> BlenderPath;
      reset_to_defaults -> OutputRegion;
      reset_to_defaults -> InputRegion;
      reset_to_defaults -> IonRegion;
      reset_to_defaults -> ConsoleRegion;
      reset_to_defaults -> Information;
   }


