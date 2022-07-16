@ECHO OFF
echo Checking if python is installed...
goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :OEF

:PYTHON_DOES_NOT_EXIST
echo It seems like you dont have python installed on your machine.
echo I'm affraid that the program won't run until python is installed.
echo the installation of python will begin now
powershell -command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe', 'C:/Tools/python-3.10.5.exe'); & c:\Tools\python-3.10.5.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=c:\Tools\Python310; [Environment]::SetEnvironmentVariable('PATH', ${env:path} + ';C:\Tools\Python310', 'Machine')"
goto :download

:PYTHON_DOES_EXIST
for /f "delims=" %%V in ('python -V') do @set ver=%%V
echo Congrats, %ver% is installed...
goto :download

:download
pip install -r requirements.txt
cd %cd%
mkdir Downloads

echo cd %cd% > yt-dl.bat
echo python main.py >> yt-dl.bat

