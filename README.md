# A simple Python script with no external dependencies to safely close all windows/programs with a single click.
## Can be used to prepare the system for shutdown or to quickly close running applications.

## Build and Run from Source

To build the executable from source, install Python 3.13.x or higher and Nuitka `pip install Nuitka`.  
Run the following command in the project directory:

```cmd
python -m nuitka --onefile --standalone --windows-console-mode=disable --assume-yes-for-downloads --output-filename=Close.exe CloseAll.py
```
