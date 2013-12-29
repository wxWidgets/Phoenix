echo off

rem This script runs all examples. This should be mostly for using the
rem examples as regression tests (after all tests have passed in tests
rem folder).
rem One command line argument is required, the python version number to
rem use, no dots: 24 for 2.4, 30 for 3.0, etc. 
rem
rem (C) Oliver Schoenborn 2009

set PY_VER=%1
IF "%1" EQU "" (
  SET PY_VER=26
  echo Will use Python 2.6. To use other, put version ID as command line arg
  echo Example: for Python 2.7 put 27, for 3.0 put 30, etc. 
)

set PYTHON_EXE=python
echo python exe is %PYTHON_EXE%

echo.
echo.
echo ######################## basic - kwargs - console #########################
echo.

pushd basic_kwargs
%PYTHON_EXE% console_main.py
popd
pause


echo.
echo.
echo ######################## basic - kwargs - wx #########################
echo.

pushd basic_kwargs
%PYTHON_EXE% wx_main.py
popd
pause


echo.
echo.
echo ######################## basic - arg1 - console #########################
echo.

pushd basic_arg1
%PYTHON_EXE% console_main.py
popd
pause


echo.
echo.
echo ######################## basic - arg1 - wx #########################
echo.

pushd basic_arg1
%PYTHON_EXE% wx_main.py
popd
pause


echo.
echo.
echo ######################## advanced - kwargs - console #########################
echo.

pushd advanced
%PYTHON_EXE% main_kwargs.py
popd
pause


echo.
echo.
echo ######################## advanced - arg1 - console #########################
echo.

pushd advanced
%PYTHON_EXE% main_arg1.py
popd
pause


