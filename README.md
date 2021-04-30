# Liberty Parser

This library provides functions to parse, manipulate and format 'Liberty' files.
The liberty format is a common standard to describe certain aspects of standard-cell libraries such as timing, power, cell pin types, etc.

Example
```python
from liberty.parser import parse_liberty

# Read and parse a library.
library = parse_liberty(open(liberty_file).read())

# Format the library.
print(str(library))
```
