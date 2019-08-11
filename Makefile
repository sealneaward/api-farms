.PHONY: help
.DEFAULT_GOAL := help

###########################################################################################################
## SCRIPTS
###########################################################################################################

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
        match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
        if match:
                target, help = match.groups()
                print("%-20s %s" % (target, help))
endef


###########################################################################################################
## VARIABLES
###########################################################################################################


export PWD=$(shell pwd)
export PROJECT_NAME="api-farms"
export PACKAGE_NAME="farm"

###########################################################################################################
## UPDATES
###########################################################################################################
build: pip-build

install: pip-install

pip-build:
	python setup.py build

pip-install:
	python setup.py install
