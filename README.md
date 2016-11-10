# libcrowds-data

[![Build Status](https://travis-ci.org/LibCrowds/libcrowds-data.svg?branch=master)]
(https://travis-ci.org/LibCrowds/libcrowds-data)
[![Coverage Status](https://coveralls.io/repos/LibCrowds/libcrowds-data/badge.svg)]
(https://coveralls.io/github/LibCrowds/libcrowds-data?branch=master)

Global data repository page for LibCrowds, designed to integrate with the
[libcrowds-pybossa-theme](https://github.com/LibCrowds/libcrowds-pybossa-theme).


## Installation

Run the following commands (modified according to your PyBossa installation directory):

```
source /home/pybossa/pybossa/env/bin/activate
cd /home/pybossa/pybossa/pybossa/plugins
git clone https://github.com/libcrowds/libcrowds-data
pip install -r libcrowds-data/requirements.txt
mv libcrowds-data/libcrowds_data libcrowds_data
rm -r libcrowds-data
```
The plugin will be available after you next restart the server.

## Configuration

The default configuration settings for libcrowds_data are:

``` Python
DATA_DISPLAY_TASKS = True
DATA_DISPLAY_TASK_RUNS = True
DATA_DISPLAY_RESULTS = True
DATA_DISPLAY_FLICKR = True
```

Each settings defines whether or not a particular item will be made available for
download via the data page. You can modify these settings by adding them to your
main PyBossa configuration file.


## Contributing

See the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to suggest improvements,
report bugs or submit pull requests.