#!/usr/bin/env python
# encoding: utf-8

################################################################################
#
#   RMG - Reaction Mechanism Generator
#
#   Copyright (c) 2009-2011 by the RMG Team (rmg_dev@mit.edu)
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the 'Software'),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
################################################################################

"""
This module contains defines the optimization model for Clar structure generation.
"""

import mipshell


class Clar(mipshell.Problem):
    def model(self, a, b, c, d, e=None):
        """
        a is number of rings
        b is number of bonds
        c is constraint matrix
        d is additional bounds on bonds
        e is additional bounds on sextet locations
        """
        # Create variable object
        x = mipshell.VarVector([a + b], 'x', type=mipshell.BIN)

        # Set object function
        mipshell.maximize(mipshell.sum_(x[i] for i in range(a)))

        # Set constraints
        for row in c:
            mipshell.sum_(row[i] * x[i] for i in range(a + b)) == 1

        for i in range(a, b):
            if d[i] is not None:
                x[i] == d[i]

        if e is not None:
            for u, v in e:
                mipshell.sum_(u[i] * x[i] for i in range(a + b)) <= v

    def getSolution(self):
        x = [var.val for var in self.vars]

        return x