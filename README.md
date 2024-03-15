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
This tutorial assumes that you already installed python and it is in your path.
### 1. Clone/download this repository
1. Go to [KavyanshKhaitan2/ipo-allotment-checker](https://github.com/KavyanshKhaitan2/ipo-allotment-checker).
2. Click on the ![Code](https://github.com/KavyanshKhaitan2/ipo-allotment-checker/assets/73186427/5356c65b-f73b-464d-a531-c52bef934f06) dropdown. 
![image](https://github.com/KavyanshKhaitan2/ipo-allotment-checker/assets/73186427/03c851bf-bd10-44c7-9a05-15a160301198)
3. Click ![Download ZIP](https://github.com/KavyanshKhaitan2/ipo-allotment-checker/assets/73186427/f98cc7dd-9adf-45b1-800b-88b6cf271e5f) button.
### 2. Make a python virtual env.
1. Make a new directory on your computer.
2. Open that directory in File Explorer.
3. Open command prompt in that directory by typing `cmd` in the address bar and hit enter.
![image](https://github.com/KavyanshKhaitan2/ipo-allotment-checker/assets/73186427/d73fa2e1-6262-4e56-b4b1-5b091dc15ad7)
4. Type the command `python -m venv ipo_allotment_checker` and hit enter.
### 3. Set-up the program
1. Open the new directory called `ipo_allotment_checker` made by that command.
2. Copy the repository you downloaded into that folder.
3. Run the following command in `ipo_allotment_checker`
   `pip install -r requirements.txt`
### 4. Done
1. Now you can use the program. Use the steps in the next section for help.

## How to use
### 1. Create new file named `panDB.txt` in the same folder as `start.bat`
### 2. Add contents to `panDB.txt`
To add content to `panDB.txt`, use the syntax seperated with newlines:
- panNo,refName
For example, Person1's pan no. is `ABCDE1234A` and Person2's pan no. is `ABDFG4567J`:
```
ABCDE1234A,Person 1
ABDFG4567J,Person 2
```
### 3. Execute `start.bat`
