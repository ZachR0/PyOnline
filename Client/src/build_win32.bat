@echo off

title Building PyOnline (Win32)...
echo ### BUILDING PYONLINE ###

echo Removing any only build / dist data...
rmdir /S /Q build > NUL
rmdir /S /Q dist > NUL

echo Building Win32 PyOnline... (make take a while)
python setup_win32.py py2exe > win32_py2exe.log

echo Moving compliled PyOnline to Deploy directory
rmdir /S /Q Deploy\win32 > NUL
mkdir Deploy\win32 > NUL
xcopy dist Deploy\win32 /e /i /h > NUL

echo Moving data resources to the Deploy directory (make take a while)
mkdir Deploy\win32\data > NUL
xcopy data Deploy\win32\data /e /i /h > NUL

echo ### BUILDING PYONLINE COMPLETE###
title PyOnline (Win32) - Done Building!
pause > NUL