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

"""
This module contains unit tests of the :mod:`arkane.gaussian` module.
"""

import os
import shutil
import unittest

from nose.plugins.attrib import attr

import rmgpy
from arkane.main import Arkane
from arkane.output import prettify


@attr('functional')
class OutputTest(unittest.TestCase):
    """
    Contains functional tests for Arkane's output module.
    """
    def test_prettify(self):
        """Test that the prettify function works for an Arkane job"""
        benzyl_path = os.path.join(os.path.dirname(os.path.dirname(rmgpy.__file__)),
                                   'examples', 'arkane', 'species', 'Benzyl')

        arkane = Arkane(input_file=os.path.join(benzyl_path, 'input.py'), output_directory=benzyl_path)
        arkane.plot = False
        arkane.execute()
        with open(os.path.join(benzyl_path, 'output.py'), 'r') as f:
            lines = f.readlines()
        self.assertIn('conformer(\n', lines)
        self.assertIn("    E0 = (193.749, 'kJ/mol'),\n", lines)
        self.assertIn('thermo(\n', lines)
        self.assertIn("        Cp0 = (33.2579, 'J/(mol*K)'),\n", lines)

    @classmethod
    def tearDownClass(cls):
        """A function that is run ONCE after all unit tests in this class."""
        benzyl_path = os.path.join(os.path.dirname(os.path.dirname(rmgpy.__file__)),
                                   'examples', 'arkane', 'species', 'Benzyl')
        extensions_to_delete = ['pdf', 'csv', 'txt', 'inp']
        files_to_delete = ['arkane.log', 'output.py']
        for name in os.listdir(benzyl_path):
            item_path = os.path.join(benzyl_path, name)
            if os.path.isfile(item_path):
                extension = name.split('.')[-1]
                if name in files_to_delete or extension in extensions_to_delete:
                    os.remove(item_path)
            else:
                if os.path.split(item_path)[-1] in ['r0']:
                    continue
                # This is a sub-directory. remove.
                shutil.rmtree(item_path)


class OutputUnitTest(unittest.TestCase):
    """
    Contains unit tests for the Arkane's output module.
    """
    def test_prettify(self):
        """Test that ``prettify`` returns the expected result"""
        input_str = ("conformer(label='C7H7', E0=(193.749,'kJ/mol'), modes=[IdealGasTranslation(mass=(91.0548,'amu')), "
                     "NonlinearRotor(inertia=([91.0567,186.675,277.733],'amu*angstrom^2'), symmetry=2), "
                     "HarmonicOscillator(frequencies=([199.381,360.536,413.795,480.347,536.285,630.723,687.118,709.613,"
                     "776.662,830.404,834.386,901.841,973.498,975.148,993.349,998.606,1040.14,1120.69,1179.22,1189.07,"
                     "1292.86,1332.91,1357.18,1479.46,1495.36,1507.91,1583.14,1604.63,3156.85,3170.22,3172.78,3185.05,"
                     "3189.8,3203.23,3253.99],'cm^-1')), HinderedRotor(inertia=(1.70013,'amu*angstrom^2'), symmetry=2, "
                     "fourier=([[-0.315923,-27.7665,0.177678,3.2437,0.0509515],[-0.00164953,-0.0021925,-0.00386396,"
                     "-0.000912068,0.00274206]],'kJ/mol'), quantum=True, semiclassical=False)], spin_multiplicity=2, "
                     "optical_isomers=1)")
        expected_output = """conformer(
    label = 'C7H7',
    E0 = (193.749, 'kJ/mol'),
    modes = [
        IdealGasTranslation(mass=(91.0548, 'amu')),
        NonlinearRotor(
            inertia = ([91.0567, 186.675, 277.733], 'amu*angstrom^2'),
            symmetry = 2,
        ),
        HarmonicOscillator(
            frequencies = ([199.381, 360.536, 413.795, 480.347, 536.285, 630.723, 687.118, 709.613, 776.662, 830.404, 834.386, 901.841, 973.498, 975.148, 993.349, 998.606, 1040.14, 1120.69, 1179.22, 1189.07, 1292.86, 1332.91, 1357.18, 1479.46, 1495.36, 1507.91, 1583.14, 1604.63, 3156.85, 3170.22, 3172.78, 3185.05, 3189.8, 3203.23, 3253.99], 'cm^-1'),
        ),
        HinderedRotor(
            inertia = (1.70013, 'amu*angstrom^2'),
            symmetry = 2,
            fourier = (
                [
                    [-0.315923, -27.7665, 0.177678, 3.2437, 0.0509515],
                    [-0.00164953, -0.0021925, -0.00386396, -0.000912068, 0.00274206],
                ],
                'kJ/mol',
            ),
            quantum = None,
            semiclassical = None,
        ),
    ],
    spin_multiplicity = 2,
    optical_isomers = 1,
)"""
        self.assertEqual(prettify(input_str), expected_output)


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
