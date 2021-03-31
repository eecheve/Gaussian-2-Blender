@echo off

set WORK_DIR=%~dp0
set BLENDER_PATH=%1
set INPUT_PATH=%2
set INPUT_NAME=%3
set OUTPUT_PATH=%4
set OUTPUT_NAME=%5
set MODEL_TYPE=%6
set OUTPUT_TYPE=%7

echo information received
echo moving on to blender path
cd
cd %BLENDER_PATH%

echo executing Main_Body script from path
blender %WORK_DIR%\ReadMolecules00.blend --background --python %WORK_DIR%\Main_Body.py -- %INPUT_PATH% %INPUT_NAME% %OUTPUT_PATH% %OUTPUT_NAME% %MODEL_TYPE% %OUTPUT_TYPE%
