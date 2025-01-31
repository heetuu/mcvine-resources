# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

PROJECT = mcvine/instruments/ARCS

# directory structure

#--------------------------------------------------------------------------
all: export
#

CP_RF = rsync -a


EXPORT_SHAREDIR=$(EXPORT_ROOT)/share
SHARE_DEST =  $(EXPORT_SHAREDIR)/$(PROJECT)

export:: export-package-data

export-package-data:: $(EXPORT_DATADIRS)
	mkdir -p $(SHARE_DEST); \
	$(CP_RF) ./ $(SHARE_DEST)/


# version
# $Id$

# End of file
