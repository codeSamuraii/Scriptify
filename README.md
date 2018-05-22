# Scriptify
Scriptify let's you convert any file into a runnable Python script.

### Introduction
#### Usage
To turn something into an executable code, use:
```
scriptify.py 'source file' 'output file' [-m] [-b] [-c [pass]] [-s msg]
```
Arguments :

- **-b** : use base64 encoding
- **-c** : encrypt file data using AES (if you don't specify a password, one will be provided to you)
- **-s** : print a custom message upon script launching
- _**-m** : use a minimal recovery script (not implemented)_

To restore the file, simply launch the script with Python.

#### Dependecies
```
pip3 install pycryptodome argparse
```

### Documentation
This project is still in early development and may contain a lot of bugs.

###### (Under construction)

### To-Do
- Documentation
- Better exception handling
- Data compression
- Dependency-less recovery script
