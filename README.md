# Scriptify
Scriptify let's you convert any file into a runnable Python script.

### Usage
To turn a file into an executable code, use:
```
scriptify.py 'source file' 'output file' [-b] [-c [pass]] [-s msg]
```
Arguments :

- **-b** : encode data using base64
- **-c** : encrypt data with AES (if no password is specified, one will be provided to you)
- **-s** : print a custom message upon script launching

To restore the file, simply launch the script with Python.

### Dependecies
- [Pycryptodome](https://pypi.org/project/pycryptodome/) : ```pip3 install pycryptodome```

### Development
##### To-Do
- Documentation
- Better exception handling

##### New versions
- Data compression
- Minimal/obfuscated recovery script
- Dependency-less recovery script
