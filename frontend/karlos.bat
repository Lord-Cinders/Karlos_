@ECHO OFF

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

IF -%2-==-- (
    ECHO,
    python "%myPath%main.py" %1 > nul 2>&1
    ECHO,
)

IF %2 == --debug GOTO :DEBUGMODE


GOTO :EOF

:DEBUGMODE
ECHO,
python "%myPath%main.py" %1 
ECHO,
GOTO :EOF

:HELP
ECHO,
python "%myPath%main.py" -h
ECHO,
GOTO :EOF
