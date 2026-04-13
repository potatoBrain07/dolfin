# Dolfin

A simple **CLI encryption tool** built in Python.  
Encrypt and decrypt files securely using Fernet encryption.

---

## Features

- Encrypt and decrypt files and directories
- Password-protected encryption
- Simple command-line interface
- Runs anywhere 

---

## Installation

Clone the repository and install it locally:

```bash
git clone https://github.com/potatoBrain07/dolfin.git
cd dolfin
pip install -e .
```

---

## Usage 

1. Encrypt or decrypt a single file
   `dolfin enc -f file.txt -p <invisible_password> #Creates file.txt.df`
   `dolfin dec -f secret.txt.df -p <invisible_password> #Restores file.txt`
2. Encrypt or decrypt files in a directory
   `dolfin enc -d directory -p <invisible_password> #All files in directory will get a .df extension`
   `dolfin dec -d directory -p <invisible_password> #All files in the directory will be restored`
3. Encrypt the directory into a single archive or decrypt the archive
   `dolfin enc -d directory --onefile -p <invisible_password> #Creates directory.df`
   `dolfin dec -d directory --onefile -p <invisible_password> #Restores directory`

**Note**: The password will not by visible during typing. 

## Dependencies

- Python 3.8+
- [cryptography](https://pypi.org/project/cryptography/)
  
Dependencies are automatically installed if you install via `pip install -e .`.

---

## License

This project is licensed under the **MIT License** - See the [LICENSE](https://github.com/potatoBrain07/dolfin/blob/main/LICENSE) file for more details.

---

## Author

[potatoBrain07](https://github.com/potatoBrain07)

---
