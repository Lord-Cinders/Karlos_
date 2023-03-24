@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

SET myPath=%~dp0

TYPE "%myPath%karlosArt.txt"

ECHO Checking for Python Installation...
reg query "hkcu\software\Python" >nul 2>&1
IF ERRORLEVEL 1 GOTO NOPYTHON
GOTO :HASPYTHON

:NOPYTHON
color 4
ECHO You dont have Python Installed. Exiting.
GOTO :EOF

:NOTSETUP
color 4
ECHO Set up Python in PATH. Exiting.

:HASPYTHON

ECHO Python is Installed, Checking if its set up...
ECHO,

python -V | find "Python" >nul 2>&1
if ERRORLEVEL 1 GOTO NOSETUP

ECHO You have Python set up.

IF -%1-==-- GOTO :HELP

SET args=
for %%x in (%*) do (
    IF %%x==--debug GOTO :DEBUGMODE
    SET args=!args!%%x 
)

python "%myPath%main.py" %args% > nul 2>&1

GOTO :EOF

:DEBUGMODE
ECHO,
python "%myPath%main.py" %args%
ECHO,
GOTO :EOF

:HELP
ECHO,
python "%myPath%main.py" -h
ECHO,
GOTO :EOF
