# Paillier Cryptosystem

## Requirements

This application was developed using Python 3.4 and the modules `gmpy2` and `pycrypto`. In order to make use of it, please check if both are available.
If you are executing the script from a GNU/Linux distro, you probably can obtain `gmpy2` through you package manager, i.e. on Ubuntu:

```
sudo apt-get install python3-gmpy2
sudo apt-get install python-pycryptopp
```

You can also use `pip` to install these, but you may be requested to install the libraries for you C compiler

```
sudo pip3 install gmpy2
sudo pip3 install pycrypto
```

## Usage

```
Usage: demo.py (--generate) [-c]
       demo.py (--encrypt | --decrypt) (<key>) (<file>) [--crt]
       demo.py -h | --help

   Arguments:
      <key>             File containing either the public 
                        or the private key.
      <file>            File to be encrypted/decrypted

   Options:
      -h --help         Displays help
      --generate        Sets key generation mode
      -c --complex      Sets complex key generation mode (default simple mode)
      --encrypt         Sets encryption mode
      --decrypt         Sets decryption mode
      --crt             Sets fast decryption mode (only on decryption)
```