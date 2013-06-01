#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2013  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from AbstractPhononKernel import AbstractPhononKernel as base

import units
meV = units.energy.meV
angstrom = units.length.angstrom


class MultiPhonon_Kernel(base):
    
    def __init__(
        self,
        dos=None,
        Qmax=None,
        ):
        base.__init__(self, dispersion=None)
        self.dos = dos
        self.Qmax = Qmax
        return
    

    def identify(self, visitor):
        return visitor.onMultiPhonon_Kernel(self)
    

    pass # end of MultiPhonon_Kernel


# version
__id__ = "$Id$"

# End of file 