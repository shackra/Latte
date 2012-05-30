Latte - Linux Automatic Time Tracker
============================

An attempt to build an automatic time tracker for Linux

[![Build Status](https://secure.travis-ci.org/flakas/Latte.png)](http://travis-ci.org/flakas/Latte)

Installation
------------

Installation is not properly supported yet. Download as a `.zip`, extract and run with `python latte/latte.py`

Configuration
-------------

Configuration scripts are saved in ~/.latte folder.

- `categories.py` should contain user defined classes for categories (see example configuration in `doc/config/categories.py`)
- `projects.py` should contain user defined classes for projects (see example configuration in `doc/config/projects.py`)


Goal
----

To build an Automatic Time Tracker for Linux that:

- keeps track of windows where the user spends time
- is aware if the user is active or not
- collects information for analysis and statistics
- Can assign time and activities to specific projects and/or categories based on
  specific rules defined by user (Regular Expressions possibly)

Tasks
-----

Tasks ordered in random manner:

- Functionality to check if the user is active (mouse and/or keyboard activity tracking)
- Functionality to check if the user is active (mouse and/or keyboard activity tracking)
- Functionality to process log data
- User defined application configuration (paths, timer durations)
- Installation
- Add comments to the code
- Add configuration examples
- Write documentation
- Add a wiki

Tasks done
----------

- Track time spent on each window
- Dump tracked time information to filesystem
- Functionality to periodically fetch window information
- Functionality to collect and periodically store activity information
- Category support
- Project support
- Automatic project/category assignment according to user defined rules

Nice to have
------------

- Python 3 support
