#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from mcni.pyre_support.Instrument import Instrument as base
class Instrument(base):

    class Inventory( base.Inventory ):

        from mcstas2.pyre_support import facility
        source = facility( 'sources', 'Source_simple', 'source' )
        monitor = facility( 'monitors', 'E_monitor', 'monitor' ) 
        pass # end of Inventory


    def __init__(self, name = 'source-monitor'):
        base.__init__(self, name)
        return
    

    def _defaults(self):
        base._defaults(self)
        self.inventory.sequence = ['source', 'monitor']
        geometer = self.inventory.geometer
        geometer.inventory.monitor = (0,0,1), (0,0,0)
        return

    
    def fini(self):
        super(Instrument, self).fini()
        monitor = self.inventory.monitor
        histogram = monitor.getFinalHistogram()
        print histogram
        return
    
    
    pass # end of Instrument



def main():
    import journal
    journal.warning('mcstas2.parsers.ComponentInfo').deactivate()
    Instrument('source-monitor').run()
    return    
    


if __name__ == "__main__":
    main()


    
# version
__id__ = "$Id$"

# End of file 
