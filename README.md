MoroccanBanksExtractor
---
Parse Moroccan banks statements into useful data formats.

#### Notes:
- **Python >= 3.10 is required.**
- Only CIH bank and Attijariwafa bank are supported for now.


## Usage
```sh
pip install -r requirements.txt
```
```
MoroccanBanksExtractor.

Usage:
    ./main.py extract [--json | --csv] <input_file>
    ./main.py mcp [--http | --stdio | --sse]
    ./main.py -h | --help
    ./main.py --version

Arguments:
    input_file     The bank statement, must be a PDF file

Options:
    -h, --help       Print this.
    --version        Print version.
```
