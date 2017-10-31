#!/usr/bin/env python
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

# Create pip-compatible dependency list from locked hashes
packages = Project().lockfile_content.get('default', {})
deps = convert_deps_to_pip(packages, r=False)

with open('requirements.txt', 'w') as f:
    f.write('\n'.join(deps))
