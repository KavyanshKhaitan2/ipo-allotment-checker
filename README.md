# ipo-allotment-checker
IPO Allotment Checker for a few registrars

## Current registrar list
+ Bigshare
+ KFintech
+ Linkintime
+ Maashitla
+ Purvashare
+ Skyline

## How to install
We introduced a new batchfile installer in the latest version.
Our current installer assumes that you already installed python and it is in your PATH.
1. Download the latest version from releases.
2. Unzip the zip file.
3. Execute the `setup.bat` file. It will install in the directory `ipo_allotment_checker` in the same folder as the `setup.bat` file.
   - NOTE**Note**: ALWAYS run `setup.bat` in the same folder as itself or it might not install correctly.
4. Installation complete
   Usually, after going through these steps, the installation should be complete.
## How to use
### 1. Create new file named `panDB.txt` in the same folder as `check_allotment.bat`
- It is usually in the `ipo_allotment_checker` directory if you used the installer
### 2. Add contents to `panDB.txt`
To add content to `panDB.txt`, use the syntax seperated with newlines:
- panNo,refName
For example, Person1's pan no. is `ABCDE1234A` and Person2's pan no. is `ABDFG4567J`:
```
ABCDE1234A,Person 1
ABDFG4567J,Person 2
```
### 3. Execute `start.bat`
