"""
Renames a list of ACCESS-ESM1.6 ocean files to the new filename pattern that
follows OM3.

Takes the list of file paths to process as command line arguments.
"""

import re
from pathlib import Path
from sys import argv


REGX = re.compile(r"(?P<realm>(ocean|ocnBgchem))\.(?P<model>.+?)\.(?P<component>.+?)(?:\.(?P<dims>\dd))?\.(?P<var>[^\.]+)\.(?P<freq>fx|\d\w{2,3})(?:\.(?P<cell_method>[^-]+?))?(?:\.y_(?P<year>\d{4}))?.nc")
TEMPLATE = "{model}.{component}{dims}.{var}.{freq}{cell_method}{year}.nc"

def build_new_name(old_name):

    m = REGX.match(old_name)
    if not m:
        raise RuntimeError(f"File {old_name} does not match the regx pattern.")

    d = m.groupdict()

    # Prepend the '.' to the optional components of the template
    for k in ['dims', 'cell_method', 'year']:
        if d.get(k):
            d[k] = '.' + d[k]

    # Replace any missing components with empty string
    for k, v in d.items():
        if v is None:
            d[k] = ""

    return TEMPLATE.format(**d)


def main():
    for filepath in argv[1:]:
        old_path = Path(filepath)

        new_name = build_new_name(old_path.name)
        new_path = old_path.parent / new_name

        print(f"{old_path.name} -> {new_name}")

        if new_path.exists():
            raise FileExistsError(f"Cannot rename {old_path} to {new_path}, file already exists")

        old_path.rename(new_path)


if __name__ == "__main__":
    main()
