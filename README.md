# Dolfin

A simple **CLI encryption tool** built in Python.  
Encrypt and decrypt files securely using Fernet encryption.

---

## Warning

- If you forget your password, your data cannot be recovered.
- Always test on dummy files before encrypting important data.
- This tool overwrites the original file.

---

## Features

- Encrypt and decrypt files
- Password-protected encryption
- Simple command-line interface
- Runs anywhere with `dolfin` command after installation

---

## Usage

- To run the program, type `dolfin` in your command prompt.

- You can run three commands in this program.
  1. To encrypt a file, run this command.
`enc path password`
Note: '\\' and ' \" ' are accepted in the path field
  2. To decrypt a file, run this program
`dec path password`
  3. To exit the program, the command is `exit`

---

## Installation

Clone the repository and install it locally:

```bash
git clone https://github.com/potatoBrain07/dolfin.git
cd dolfin
pip install -e .
```

---

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
