# Scriptify
Scriptify let's you convert any file into a runnable Python script.

### Usage
To turn something into an executable code, use:
```
scriptify.py 'source file' 'output file' [-m] [-b] [-c [pass]] [-s msg]
```
Arguments :
- _**-m** : use a minimal recovery script (not implemented)_
- **-b** : use base64 encoding
- **-c** : encrypt file data using AES (if you don't specify a password, one will be provided to you)
- **-s** : print a custom message upon script launching

To restore the file, simply launch the script with Python.

###### Following is outdated.
### Features
This project is still in early developpement. While changing the file format and hidding it's content, the current output script does not provide any protection for your data or improvements in file size.

New features coming with version 0.2:
- _**Data encryption** w/ password_
- _Custom message display when script is run_
- _Base64 data encoding_

In future versions:
- _**Data compression** and signature_
- _Minimal container script_

_..._
