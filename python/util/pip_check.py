
import os
import pkg_resources
import vim
from pkg_resources import DistributionNotFound, VersionConflict

###
# This was obtained from https://stackoverflow.com/questions/16294819/check-if-my-python-has-all-required-packages 
###

# dependencies can be any iterable with strings, 
# e.g. file line-by-line iterator
dependencies = []
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + "/../../requirements.txt", 'rb') as f:
    for line in f:
        requirement = line.decode('ascii').rstrip()
        if requirement:
            dependencies += [requirement]

# here, if a dependency is not met, a DistributionNotFound or VersionConflict
# exception is thrown. 
try:
    pkg_resources.require(dependencies)
except (DistributionNotFound, VersionConflict) as e:
    print(e)
    print("Please consult the 'jiravim-pip-install' help tag for help on installing pip dependencies")
