@echo off

set WORK_DIR=%~dp0
set BLENDER_PATH=%1

echo information received
echo moving on to blender path
cd
cd %BLENDER_PATH%

echo executing Receive_Parameters script from path
blender %WORK_DIR%\ReadMolecules00.blend --background --python %WORK_DIR%\Receive_Parameters.py