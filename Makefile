# Makefile Helper for setting up the benchmarking framework
# Author: Manuel Bernal Llinares <mbdebian@gmail.com>
all:
	@echo "<===|DEVOPS|===> [ALL] There is no default target for this helper"

install_requirements:
	@echo "<===|DEVOPS|===> [INSTALL] Installing Application Requirements"
	@python_install/bin/pip install pipreqs nose
	@python_install/bin/pip install -r requirements.txt

python_install:
	@echo "<===|DEVOPS|===> [INSTALL] Python Virtual Environment"
	@pip install --user virtualenv
	@virtualenv python_install

install: dev_environment
	@echo "<===|DEVOPS|===> [INSTALL] Initializing Application Installation"

# Folders
tmp:
	@echo "<===|DEVOPS|===> [MKDIR] Temporary folder"
	@mkdir tmp

# Environments
dev_environment: python_install install_requirements
	@echo "<===|DEVOPS|===> [INSTALL] Development Environment"

# Dependencies
update_requirements_file: dev_environment
	@echo "<===|DEVOPS|===> [UPDATE] Application Requirements"
	#@python_install/bin/pipreqs --use-local --savepath requirements.txt $(PWD)
	@python_install/bin/pip freeze > requirements.txt
