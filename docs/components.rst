Program Architecture
========================
TheorChem2Blender is handled by two main python scripts that comunicate with each other by a OS-dependent executable script.
The API is handled by Main_Body.py, and the GUI by TheorChem2Blender.py. The two scripts are linked by either ReadMolecules.bat
(Windows) or ReadMolecules.sh (MacOS). Below are five UML component diagrams illustrating the broad structure of the program:
the overall outline, the Blender-side API (split into its core molecule-building pipeline and its unit cell/crystallography
pipeline, since the latter only activates for ``.vasp`` input), the GUI, and the console/logging relay that ties the two
processes' output together.

- The main scripts are shown in gray.
- The principal functions called are shown in light blue.
- The modules associated with each function are displayed in light green.
- Data or parameter files are purple.

Methods that exist in the code but are never actually called anywhere in the current program flow (dead/orphaned code) are
left out of these diagrams entirely, so that what's drawn always matches what actually runs.

Program Outline
----------------

.. graphviz::

   digraph Outline {
         rankdir = LR;
         node [shape=box, style=filled];

         Main_Body [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];
         TheorChem2Blender [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];

         Ionic_py [label="Ionic.py\n(GUI ion dropdown data)", fillcolor=lavender];
         Atom_Data_py [label="Atom_Data.py\n(covalent/VdW/ionic radii)", fillcolor=lavender];
         covalent_radii_json [label="covalent_radii.json\n(external_data/, bond-order detection)", fillcolor=lavender];

         t2b_config [fillcolor=lavender];

         ReadMolecules_bat [fillcolor=lightgreen];
         ReadMolecules_sh [fillcolor=lightgreen];

         if_windows [shape=box, style=filled, fillcolor=white, color=white];
         if_mac_os [shape=box, style=filled, fillcolor=white, color=white];

         Ionic_py -> TheorChem2Blender;

         TheorChem2Blender -> t2b_config;

         t2b_config -> if_windows;
         t2b_config -> if_mac_os;

         if_windows -> ReadMolecules_bat;
         if_mac_os -> ReadMolecules_sh;

         ReadMolecules_bat -> Main_Body;
         ReadMolecules_sh -> Main_Body;
         Atom_Data_py -> Main_Body;
         covalent_radii_json -> Main_Body;
   }


Blender API
------------------------
Main_Body.py's own logic is split across two diagrams. The core pipeline below covers parsing an input file (regardless of
type), preparing atoms/bonds/ions/materials, and building/highlighting/animating/exporting one growth cell. The unit cell
and crystallography diagram that follows it covers what happens *inside* that same per-export step when the input is a
``.vasp`` file with unit cell features enabled - it is entirely skipped otherwise.

Core Pipeline
~~~~~~~~~~~~~~

.. graphviz::

   digraph API_Core {
       node [shape=box, style=filled];

       Main_Body [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];

       Obtain_Coords_Connect [fillcolor=lightblue];
       Overwrite_Bonds_if_Needed [fillcolor=lightblue];
       Prepare_Atoms_and_Bonds [fillcolor=lightblue];
       Prepare_Ions [fillcolor=lightblue];
       Get_Growth_Specs [fillcolor=lightblue];
       Build_And_Export_Growth_Cell [fillcolor=lightblue];
       Read_com_File [fillcolor=lightblue];
       Refine_com_File [fillcolor=lightblue];
       Read_xyz_File [fillcolor=lightblue];
       Read_mol2_File [fillcolor=lightblue];
       Read_vasp_File [fillcolor=lightblue];
       Build_Molecule [fillcolor=lightblue];
       Highlight_Atoms [fillcolor=lightblue];
       Highlight_Bonds [fillcolor=lightblue];
       Animate [fillcolor=lightblue];
       Manage_Export [fillcolor=lightblue];

       Raw_Parameters [fillcolor=lightgreen];
       Refine_Data [fillcolor=lightgreen];
       XyzReader [fillcolor=lightgreen];
       Mol2Reader [fillcolor=lightgreen];
       VaspReader [fillcolor=lightgreen];
       BondOverwriter [fillcolor=lightgreen];
       Refine_Elements [fillcolor=lightgreen];
       Atom_Data [fillcolor=lightgreen];
       Create_Materials [fillcolor=lightgreen];
       Ions [fillcolor=lightgreen];
       Instantiate_Molecules [fillcolor=lightgreen];
       Primitives [fillcolor=lightgreen];
       AtomHighlighter [fillcolor=lightgreen];
       Animate_Module [label="Animate", fillcolor=lightgreen];
       SceneCleaner [fillcolor=lightgreen];
       Export_Data [fillcolor=lightgreen];

       UnitCell_Crystallography [label="Unit Cell &\nCrystallography steps\n(see next diagram)",
                                  shape=box, style="filled,dashed", fillcolor=white];

       Main_Body -> Obtain_Coords_Connect;
       Main_Body -> Overwrite_Bonds_if_Needed;
       Main_Body -> Prepare_Atoms_and_Bonds;
       Main_Body -> Prepare_Ions;
       Main_Body -> Get_Growth_Specs;
       Get_Growth_Specs -> Build_And_Export_Growth_Cell [label="once per\ngrowth spec"];

       Obtain_Coords_Connect -> Read_com_File;
       Obtain_Coords_Connect -> Read_xyz_File;
       Obtain_Coords_Connect -> Read_mol2_File;
       Obtain_Coords_Connect -> Read_vasp_File;
       Read_com_File -> Refine_com_File;
       Read_com_File -> Raw_Parameters;
       Refine_com_File -> Refine_Data;
       Read_xyz_File -> XyzReader;
       Read_mol2_File -> Mol2Reader;
       Read_vasp_File -> VaspReader;

       Overwrite_Bonds_if_Needed -> BondOverwriter;

       Prepare_Atoms_and_Bonds -> Refine_Elements;
       Prepare_Atoms_and_Bonds -> Atom_Data;
       Prepare_Atoms_and_Bonds -> Create_Materials;

       Prepare_Ions -> Refine_Elements;
       Prepare_Ions -> Atom_Data;
       Prepare_Ions -> Ions;

       Build_And_Export_Growth_Cell -> SceneCleaner [label="clears scene\nbefore each export"];
       Build_And_Export_Growth_Cell -> Build_Molecule;
       Build_And_Export_Growth_Cell -> Highlight_Atoms;
       Build_And_Export_Growth_Cell -> Highlight_Bonds;
       Build_And_Export_Growth_Cell -> Animate;
       Build_And_Export_Growth_Cell -> Manage_Export;
       Build_And_Export_Growth_Cell -> UnitCell_Crystallography;

       Build_Molecule -> Instantiate_Molecules;
       Instantiate_Molecules -> Primitives;

       Highlight_Atoms -> AtomHighlighter;
       Highlight_Bonds -> AtomHighlighter;

       Animate -> Animate_Module;

       Manage_Export -> Animate_Module;
       Manage_Export -> Export_Data;
   }

Unit Cell & Crystallography
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Everything below runs only when the input is a ``.vasp`` file with the relevant Unit Cells tab options enabled - for any
other input type these steps are no-ops. All of it happens inside the same ``Build_And_Export_Growth_Cell`` step shown in
the core pipeline diagram, once per growth-cell size the user configured.

.. graphviz::

   digraph API_UnitCell {
       node [shape=box, style=filled];

       Build_And_Export_Growth_Cell [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];

       Build_Unit_Cell [fillcolor=lightblue];
       Replicate_Unit_Cell [fillcolor=lightblue];
       Link_Unit_Cells [fillcolor=lightblue];
       Delete_Forbidden_Bonds [fillcolor=lightblue];
       Build_Polyhedra [fillcolor=lightblue];
       Build_Miller_Planes [fillcolor=lightblue];
       Build_Miller_Plane [fillcolor=lightblue];
       Parent_Bounding_Box [fillcolor=lightblue];

       BoundBoxBuilder [fillcolor=lightgreen];
       UnitCellReplicator [fillcolor=lightgreen];
       UnitCellLinker [fillcolor=lightgreen];
       Primitives [fillcolor=lightgreen];
       BondOverwriter [fillcolor=lightgreen];
       PolyhedronBuilder [fillcolor=lightgreen];
       MillerPlaneBuilder [fillcolor=lightgreen];

       Build_And_Export_Growth_Cell -> Build_Unit_Cell [label="if unit cell\nboundaries checked"];
       Build_And_Export_Growth_Cell -> Replicate_Unit_Cell [label="if growth\nrepeats > 1x1x1"];
       Build_And_Export_Growth_Cell -> Link_Unit_Cells [label="if growth\nrepeats > 1x1x1"];
       Build_And_Export_Growth_Cell -> Delete_Forbidden_Bonds [label="if custom\nthresholds set"];
       Build_And_Export_Growth_Cell -> Build_Polyhedra [label="if polyhedra\ncenters set"];
       Build_And_Export_Growth_Cell -> Build_Miller_Planes;
       Build_And_Export_Growth_Cell -> Parent_Bounding_Box;

       Build_Unit_Cell -> BoundBoxBuilder;
       Parent_Bounding_Box -> BoundBoxBuilder;

       Replicate_Unit_Cell -> UnitCellReplicator;

       Link_Unit_Cells -> UnitCellLinker;
       Link_Unit_Cells -> Primitives;

       Delete_Forbidden_Bonds -> BondOverwriter;

       Build_Polyhedra -> PolyhedronBuilder;

       Build_Miller_Planes -> Build_Miller_Plane;
       Build_Miller_Plane -> MillerPlaneBuilder;
   }


GUI
----
TheorChem2Blender.py's own logic, rewritten to match the current queue-based conversion flow: clicking ``Convert!`` no
longer blocks the GUI while Blender runs - it queues one file at a time and lets a background thread launch each Blender
subprocess while the main thread keeps polling for completion.

.. graphviz::

   digraph GUI {
      node [shape=box, style=filled];

      TheorChem2Blender [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];

      convert [fillcolor=lightblue];
      convert_manager [fillcolor=lightblue];
      exceptions_test_passed [fillcolor=lightblue];
      assign_ionic_params [fillcolor=lightblue];
      start_conversion_queue [label="_start_conversion_queue", fillcolor=lightblue];
      run_next_conversion [label="_run_next_conversion", fillcolor=lightblue];
      run_blender_subprocess [label="_run_blender_subprocess", fillcolor=lightblue];
      check_conversion_thread [label="_check_conversion_thread", fillcolor=lightblue];
      input_to_json [fillcolor=lightblue];
      populate_animation_frames [fillcolor=lightblue];
      populate_unit_cell_repeats [fillcolor=lightblue];
      populate_miller_indices [fillcolor=lightblue];
      reset_to_defaults [fillcolor=lightblue];
      handle_animation_toggle [fillcolor=lightblue];
      handle_input_type_change [fillcolor=lightblue];

      BlenderPath [fillcolor=lightgreen];
      InputRegion [fillcolor=lightgreen];
      HighlighterRegion [fillcolor=lightgreen];
      OutputRegion [fillcolor=lightgreen];
      IonRegion [fillcolor=lightgreen];
      UnitCellRegion [fillcolor=lightgreen];
      ActionsRegion [fillcolor=lightgreen];
      Coordinates [fillcolor=lightgreen];

      TheorChem2Blender -> convert;
      TheorChem2Blender -> reset_to_defaults;
      TheorChem2Blender -> handle_animation_toggle;
      TheorChem2Blender -> handle_input_type_change;

      convert -> convert_manager;

      convert_manager -> BlenderPath;
      convert_manager -> InputRegion;
      convert_manager -> HighlighterRegion;
      convert_manager -> OutputRegion;
      convert_manager -> UnitCellRegion;
      convert_manager -> exceptions_test_passed;
      convert_manager -> assign_ionic_params;
      convert_manager -> start_conversion_queue;

      assign_ionic_params -> IonRegion;
      assign_ionic_params -> UnitCellRegion;

      start_conversion_queue -> ActionsRegion [label="disable\nConvert!"];
      start_conversion_queue -> run_next_conversion;

      run_next_conversion -> input_to_json;
      run_next_conversion -> run_blender_subprocess [label="background\nthread"];
      run_next_conversion -> check_conversion_thread;
      run_next_conversion -> ActionsRegion [label="re-enable Convert!\n(queue empty)"];

      check_conversion_thread -> run_next_conversion [label="poll via\nroot.after()", style=dashed];

      input_to_json -> InputRegion;
      input_to_json -> populate_animation_frames;
      input_to_json -> populate_unit_cell_repeats;
      input_to_json -> populate_miller_indices;

      populate_animation_frames -> Coordinates;

      reset_to_defaults -> BlenderPath;
      reset_to_defaults -> OutputRegion;
      reset_to_defaults -> InputRegion;
      reset_to_defaults -> HighlighterRegion;
      reset_to_defaults -> IonRegion;

      handle_animation_toggle -> OutputRegion;
      handle_animation_toggle -> InputRegion;

      handle_input_type_change -> UnitCellRegion [label="enable/disable\ntab"];
   }


Console & Logging Relay
-------------------------
This one doesn't fit the function-call shape of the other diagrams, since nothing calls it directly - every ``print()``
anywhere in the GUI process flows through it automatically, and it also tails whatever the separate Blender subprocess
writes. It exists so long-running conversions (large batches, growth-cell exports, animations) show live progress instead
of the GUI appearing frozen.

.. graphviz::

   digraph Logging {
       node [shape=box, style=filled];

       TheorChem2Blender [fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];
       Main_Body [label="Main_Body\n(separate Blender\nsubprocess)", fillcolor=gray, fontcolor=white, color=black, style=filled, shape=box];

       print_calls [label="print() calls\n(anywhere in the\nGUI process)", fillcolor=lightblue];

       ConsoleRegion [fillcolor=lightgreen];
       TextRedirector [fillcolor=lightgreen];

       output_log [label="output.log", fillcolor=lavender];

       TheorChem2Blender -> ConsoleRegion [label="instantiates,\nwires sys.stdout"];
       ConsoleRegion -> TextRedirector [label="constructs with\nlog_path=output.log"];
       print_calls -> TextRedirector [label="redirected via\nsys.stdout"];
       TextRedirector -> output_log [label="tees every line"];

       Main_Body -> output_log [label="stdout redirected by\n_run_blender_subprocess", style=dashed];

       output_log -> ConsoleRegion [label="poll_log_file()\nevery 500ms", style=dashed];
   }
