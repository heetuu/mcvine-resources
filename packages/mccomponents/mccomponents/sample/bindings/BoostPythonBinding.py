#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from mccomponents.homogeneous_scatterer.bindings.BoostPythonBinding \
     import BoostPythonBinding, extend

import mccomponents.mccomponentsbp as b
import mccomposite.mccompositebp as b1


class New:

    def gridsqe(self, qbegin, qend, qstep,
                ebegin, eend, estep,
                s ):
        '''gridsqe: S(Q,E) on grid

        qbegin, qend, qstep: Q axis
        ebegin, eend, estep: E axis
        s: numpy array of S
        '''
        shape = s.shape
        assert len(shape) == 2
        assert shape[0] == int( (qend-qbegin)/qstep )
        assert shape[1] == int( (eend-ebegin)/estep )
        size = shape[0] * shape[1]
        
        svector = b.vector_double( size )
        s.shape = -1,
        svector[:] = s
        
        fxy = b.new_fxy(
            qbegin, qend, qstep,
            ebegin, eend, estep,
            svector)
        
        return b.GridSQE( fxy )

    
    def sqekernel(self, absorption_cross_section, scattering_cross_section,
                  sqe, Qrange, Erange):
        '''sqekernel: a kernel takes S(Q,E) a functor

        absorption_cross_section: absorption cross section
        scattering_cross_section: scattering cross section
        sqe: S(Q,E) functor
        Qrange, Erange: range of Q and E
        '''
        Emin, Emax = Erange
        Qmin, Qmax = Qrange
        return b.SQEkernel(
            absorption_cross_section, scattering_cross_section,
            sqe, Qmin, Qmax, Emin, Emax )
    

    pass # end of BoostPythonBinding


extend( New )



# version
__id__ = "$Id$"

# End of file 