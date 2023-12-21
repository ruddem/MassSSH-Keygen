# Python-Tool to generate a ton of encrypted SSH-Keys
## Description
Following output for every SSH-Key-Pair:
- $KEYNAME.ppk
- $KEYNAME.pub
- $KEYNAME.key
- $KEYNAME.pass
(.pass contains password for the encrypted private-key)

> [!NOTE]
> It only supports ED25519 and RSA Keys

Keyname is composed of the following patterns:
Date(YYYYMMDD) and 16 random letters/numbers.
Example:
- 20231221_3a6e44faad62ac7e.ppk
- 20231221_3a6e44faad62ac7e.pub
- 20231221_3a6e44faad62ac7e.key
- 20231221_3a6e44faad62ac7e.pass

## Before Usage:
Make sure that the packages "putty-tools" and "python3" are installed on the Unix system.

## Tested executable under the following systems:
- Debian 11
- Debian 11 (WSL)
- Debian 12

## Usage:
```text
python3 main.py
```
(If the optional parameters are not specified, the variables set in config.py are used)

```text
python3 main.py [-h] [-l GENERATED_FILES_LOCATION] [-g KEYS_TO_GENERATE] [-d {True,False}]
```

```text
optional arguments:\
  -h, --help            show this help message and exit\
  -l GENERATED_FILES_LOCATION, --generated_files_location GENERATED_FILES_LOCATION\
                        Define save location for generated Files (default='keys/')\
  -g KEYS_TO_GENERATE, --keys_to_generate KEYS_TO_GENERATE\
                        Define number of keys to generate (default='1')\
  -d {True,False}, --dry {True,False}\
                        dry run script, only print in cli (default='False')\
  -t {ed25519,rsa}, --key_type {ed25519,rsa}\
                        specify key type when generating (ed25519, rsa) (default='ed25519')
```
