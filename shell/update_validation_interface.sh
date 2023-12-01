#!/bin/bash

# Download nodejs modules for the validation interface.

# Give permission to run this script with:
# chmod a+x shell/update_validation_interface.sh

echo -e "\nInstalling validation interface node modules...\n"

cd validation-interface
npm install
cd ../


echo -e "Validation interface ready!\n"