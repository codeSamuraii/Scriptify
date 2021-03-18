# Scriptify
Scriptify converts any file into a runnable Python script that will restore the original file when run.

### Usage
To turn a file into an executable code, use:
```
scriptify.py 'source file' 'output file' [-m] [-c[c]] [-p [pass]] [-s msg]
```
Arguments :

- **-m** : minimal recovery script
- **-c** : use LZMA compression for file data (may be used twice to increase compression)
- **-p** : encrypt data with AES (if no password is specified, one will be provided to you)
- **-s** : print a custom message upon script launching

To restore the file, simply launch the script with Python.

### Dependecies
- [Pycryptodome](https://pypi.org/project/pycryptodome/) : ```pip3 install pycryptodome```
- [pyminifier](https://github.com/liftoff/pyminifier) : ```pip3 install pyminifier```

### Development
##### To-Do
- Documentation
- Memory improvements
- Better compression
- Exception handling

##### New versions
- Obfuscated recovery script
- Dependency-less recovery script
