# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = mccomponents
PACKAGE = tests

PROJ_CLEAN += $(PROJ_CPPTESTS)

PROJ_PYTESTS =  alltests.py
PROJ_CPPTESTS = \
	test_fparser \
	test_random \
	test_rootfinding \

PROJ_TESTS = $(PROJ_PYTESTS) $(PROJ_CPPTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) -ljournal -lmcni -lmccomposite -lmcstas_compact -lmccomponents -lfparser


#--------------------------------------------------------------------------
#

all: $(PROJ_TESTS)

test:
	for test in $(PROJ_TESTS) ; do $${test}; done

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#

test_random: test_random.cc
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_random.cc $(PROJ_LIBRARIES)

test_rootfinding: test_rootfinding.cc
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_rootfinding.cc $(PROJ_LIBRARIES)

test_fparser: test_fparser.cc
	$(CXX) $(CXXFLAGS) $(LCXXFLAGS) -o $@ test_fparser.cc $(PROJ_LIBRARIES)


# version
# $Id$

# End of file
