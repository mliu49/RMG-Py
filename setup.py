#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#                                                                             #
# RMG - Reaction Mechanism Generator                                          #
#                                                                             #
# Copyright (c) 2002-2019 Prof. William H. Green (whgreen@mit.edu),           #
# Prof. Richard H. West (r.west@neu.edu) and the RMG Team (rmg_dev@mit.edu)   #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining a     #
# copy of this software and associated documentation files (the 'Software'),  #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included in  #
# all copies or substantial portions of the Software.                         #
#                                                                             #
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
#                                                                             #
###############################################################################

import sys
import os

try:
    from distutils.core import setup
    from distutils.extension import Extension
except ImportError:
    print 'The distutils package is required to build or install RMG Py.'
    
try:
    from Cython.Build import cythonize
    from Cython.Compiler import Options
except ImportError:
    print 'Cython (http://www.cython.org/) is required to build or install RMG Py.'
    
try:
    import numpy
except ImportError:
    print 'NumPy (http://numpy.scipy.org/) is required to build or install RMG Py.'

# Create annotated HTML files for each of the Cython modules
Options.annotate = True

directives = {
    # Set language to python 2
    'language_level': 2,
    # Turn on profiling capacity for all Cython modules
    # 'profile': True,
    # Embed docstrings in cythonized files - enable when building documentation
    # 'embedsignature': True,
}

################################################################################


main_ext_modules = [
    # Kinetics
    'rmgpy/kinetics/*.pyx',
    # Chemical representations
    'rmgpy/molecule/*.pyx',
    'rmgpy/molecule/atomtype.py',
    'rmgpy/molecule/converter.py',
    'rmgpy/molecule/element.py',
    'rmgpy/molecule/group.py',
    'rmgpy/molecule/inchi.py',
    'rmgpy/molecule/molecule.py',
    'rmgpy/molecule/pathfinder.py',
    'rmgpy/molecule/resonance.py',
    'rmgpy/molecule/symmetry.py',
    'rmgpy/molecule/translator.py',
    'rmgpy/molecule/util.py',
    # Pressure dependence
    'rmgpy/pdep/*.pyx',
    # Statistical mechanics
    'rmgpy/statmech/*.pyx',
    # Thermodynamics
    'rmgpy/thermo/*.pyx',
    # Miscellaneous
    'rmgpy/*.pyx',
    'rmgpy/constants.py',
    'rmgpy/quantity.py',
    'rmgpy/reaction.py',
    'rmgpy/species.py',
]

solver_ext_modules = [
    'rmgpy/solver/*.pyx',
]

arkane_ext_modules = [
    # Kinetics
    'rmgpy/kinetics/*.pyx',
    # Pressure dependence
    'rmgpy/pdep/*.pyx',
    # Statistical mechanics
    'rmgpy/statmech/*.pyx',
    # Thermodynamics
    'rmgpy/thermo/*.pyx',
    # Miscellaneous
    'rmgpy/*.pyx',
    'rmgpy/constants.py',
    'rmgpy/quantity.py',
    'rmgpy/reaction.py',
    'rmgpy/species.py',
]

################################################################################

ext_modules = []
if 'install' in sys.argv:
    # This is so users can still do simply `python setup.py install`
    ext_modules.extend(main_ext_modules)
    ext_modules.extend(solver_ext_modules)
if 'main' in sys.argv:
    # This is for `python setup.py build_ext main`
    sys.argv.remove('main')
    ext_modules.extend(main_ext_modules)
if 'solver' in sys.argv:
    # This is for `python setup.py build_ext solver`
    sys.argv.remove('solver')
    ext_modules.extend(solver_ext_modules)
if 'arkane' in sys.argv:
    # This is for `python setup.py build_ext arkane`
    sys.argv.remove('arkane')
    ext_modules.extend(main_ext_modules)
    ext_modules.extend(arkane_ext_modules)
if 'minimal' in sys.argv:
    # This starts with the full install list, but removes anything that has a pure python mode
    # i.e. in only includes things whose source is .pyx
    sys.argv.remove('minimal')
    temporary_list = []
    temporary_list.extend(main_ext_modules)
    temporary_list.extend(solver_ext_modules)
    for module in temporary_list:
        for source in module.sources:
            if os.path.splitext(source)[1] == '.pyx':
                ext_modules.append(module)

scripts=['Arkane.py',
         'rmg.py',
         'scripts/checkModels.py',
         'scripts/convertFAME.py',
         'scripts/diffModels.py',
         'scripts/generateChemkinHTML.py',
         'scripts/generateFluxDiagram.py',
         'scripts/generateReactions.py',
         'scripts/machineWriteDatabase.py',
         'scripts/mergeModels.py',
         'scripts/simulate.py',
         'scripts/standardizeModelSpeciesNames.py',
         'scripts/thermoEstimator.py',
         'testing/databaseTest.py']

modules = []
for root, dirs, files in os.walk('rmgpy'):
    if 'test_data' in root:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.pyx'):
            if 'Test' not in file and '__init__' not in file:
                module = 'rmgpy' + root.partition('rmgpy')[-1].replace('/','.') + '.' + file.partition('.py')[0]
                modules.append(module)
for root, dirs, files in os.walk('arkane'):
    if 'data' in root:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.pyx'):
            if 'Test' not in file and '__init__' not in file:
                module = 'arkane' + root.partition('arkane')[-1].replace('/','.') + '.' + file.partition('.py')[0]
                modules.append(module)

# Read the version number
exec(open('rmgpy/version.py').read())

# Initiate the build and/or installation
setup(
    name='RMG-Py',
    version=__version__,
    description='Reaction Mechanism Generator',
    author='William H. Green and the RMG Team',
    author_email='rmg_dev@mit.edu',
    url='http://reactionmechanismgenerator.github.io',
    packages=['rmgpy','arkane'],
    py_modules = modules,
    scripts=scripts,
    ext_modules=cythonize(ext_modules, build_dir='build/cython', compiler_directives=directives),
    include_dirs=['.', numpy.get_include()],
)
