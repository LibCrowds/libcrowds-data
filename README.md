# libcrowds-data

[![Build Status](https://travis-ci.org/LibCrowds/libcrowds-data.svg?branch=master)](https://travis-ci.org/LibCrowds/libcrowds-data)
[![Coverage Status](https://coveralls.io/repos/LibCrowds/libcrowds-data/badge.svg)](https://coveralls.io/github/LibCrowds/libcrowds-data?branch=master)

Global data repository page for LibCrowds, designed to integrate with the 
[libcrowds-bs4-pybossa-theme](https://github.com/LibCrowds/libcrowds-bs4-pybossa-theme).


## Installation

Run the following commands (modified according to your PyBossa installation directory):

```
source /home/pybossa/pybossa/env/bin/activate
cd /home/pybossa/pybossa/pybossa/plugins
git clone https://github.com/libcrowds/libcrowds-data
pip install -r libcrowds-data/requirements.txt
ln -s libcrowds-data/libcrowds_data libcrowds_data
```
The plugin will be available after you next restart the server.

## Contributing

See the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to suggest improvements,
report bugs or submit pull requests.
