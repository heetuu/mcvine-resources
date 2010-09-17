# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# McStas component format: http://neutron.risoe.dk/documentation/mcdoc/

"""
McStasComponentParser - parser for McStas components

Declarations:
    - First comment is considered to be a header!
    - Stars in the header might not need to start from the very beginning
      starting spaces allowed: '*' and ' *' have the same effect
    - Input and output parameters are separated from the corresponding
      decsription by semicolumn with format: <name>:{spaces}<description>
        Example: "xmin:     Lower x bound of detector opening (m)"
    - Sections can be in arbitrary order
    - Descriptions (short and full) CANNOT have ':' character!
    - Example parameter should be in Description section

Notes:
    -
"""

import re

# Utils
def paramRegex(name):
    "Returns parameter regex specified by name"
    return "^(%s):([^\n]*)" % name

# Constants
INFO            = "%I"
DESCRIPTION     = "%D"
PARAMS          = "%P"
END             = "%E"
SECTIONS        = [INFO, DESCRIPTION, PARAMS] # Standard order
DIRECTIVES      = SECTIONS + [END,]
COPYRIGHT_N     = "Written by"
DATE_N          = "Date"
VERSION_N       = "Version"
ORIGIN_N        = "Origin"
RELEASE_N       = "Release"

# Allowed info parameters
STD_PARAMS      = [DATE_N, VERSION_N, ORIGIN_N, RELEASE_N]
INFO_PARAMS     = STD_PARAMS + [COPYRIGHT_N,]

INPUT_PARAMS    = "INPUT PARAMETERS"
OUTPUT_PARAMS   = "OUTPUT PARAMETERS"

# Regular expressions
COMMENT         = '(/\*.*?\*/)'             # Non-greedy comment (.*?)
SPACES          = '[ \t]*'                  # Spaces and tabs
WINCR           = '\r'                      # Window's CR
STAR            = "^%s[\*]*%s" % (SPACES, SPACES)   # Starting stars
PARAM           = "^([^\:]*?):([^\n]*)"     # Parameter
COMP_NAME       = "Component:([^\n]*)\n\n"  # Component name
EXAMPLE         = "Example:(.*?)\n\n"    # Example

INFO_SEC        = "%s(.*?)(?=%s|%s|%s)" % (INFO, DESCRIPTION, PARAMS, END)  # Info section
DESC_SEC        = "%s(.*?)(?=%s|%s|%s)" % (DESCRIPTION, INFO, PARAMS, END)  # Description section
PARAM_SEC       = "%s(.*?)(?=%s|%s|%s)" % (PARAMS, INFO, DESCRIPTION, END)  # Parameters section



class McStasComponentParser:

    def __init__(self, filename=None, config=None, parse=True):
        self._filename      = filename
        self._config        = config
        # OrderedDict?
        self._header        = {}
        self._inputparams   = {}
        self._outputparams  = {}

        if parse and (self._fileExists() or config):
            self.parse()        


    def parse(self):
        """
        Parses config string or file and appends component to self._components

        Algorithm steps:
        - Extract header (first /*...*/ comment)
        - Remove stars and spaces after them ('*{spaces}' -> '')
        - Remove '\r' for Windows files
        - Find first occurence of pattern: "Component: ...\n" and cut the part above it
          and replace by empty string ""
        - Split by lines and go over them to populate header dict
        - Find first occurence of pattern: "Example: ...{no DIRECTIVES}" and cut the part above it
          and replace by empty string ""
        """

        configText   = self._configText()

        p           = re.compile(COMMENT, re.DOTALL)
        matches     = p.findall(configText)
        if len(matches) < 1: # No header
            return

        text        = matches[0]                # First comment is the header
        text        = self._strip(WINCR, text)     # Strip carriage return
        headertext  = self._strip(STAR, text)   # Strip stars
        compname    = self._compName(headertext)

        info        = self._sectionText(INFO_SEC, headertext)
        desc        = self._sectionText(DESC_SEC, headertext)
        param       = self._sectionText(PARAM_SEC, headertext)

        self._parseInfoSection(info)
        self._parseDescSection(desc)
        self._parseParamSection(param)
        
        # Names are kept for backward compatibility
        self._header["componentname"]    = compname

#        self._header["full_description"]    = ""

#        self._header["input_parameters"]    = self._inputparams
#        self._header["output_parameters"]    = self._outputparams



    def header(self):
        return self._header


    def toString(self, br="\n"):
        str     = ""
        for (key, value) in self._header.iteritems():
            str += "%s: %s%s" % (key, value, br)

        return str


    def _configText(self):
        "Take config from file if it exist and readable, or use from config - otherwise"
        configText  = ""
        if self._fileExists():
            try:        # Try to read it
                configText  = open(self._filename).read()
            except:
                pass    # No exception
            return configText

        if self._config:
            configText  = self._config

        return configText   # Empty string


    def _fileExists(self):
        "Checks if file exists"
        if self._filename and os.path.exists(self._filename):
            return True

        return False


    def _strip(self, regex, text):
        "Strips piece of text that matches regex pattern"
        p   = re.compile(regex, re.DOTALL|re.MULTILINE)
        s   = re.sub(p, '', text)
        return s


    def _compName(self, text):
        p           = re.compile(COMP_NAME, re.IGNORECASE)
        namefinds   = p.findall(text)
        if not namefinds:
            return ""    # Empty name
        
        name    = namefinds[0].strip()
        return name


    def _sectionText(self, secregex, text):
        "Returns section string that matches secregex pattern"
        p           = re.compile(secregex, re.DOTALL)
        matches     = p.findall(text)
        if len(matches) < 1: # No section found, return empty string
            return ""
        
        return matches[0]   # Return the first found match


    def _parseInfoSection(self, text):
        "Parses info section and populates part of header parameters"
        # XXX: There might be problems that description has ':' character
        #           In this case check if numbr == 2 and afterparam = True
        lines       = text.split("\n")

        for l in lines:
            l   = l.strip()
            if l == '':
                continue    # Skip empty line

            p   = re.compile(PARAM)
            m   = p.match(l)
            
            if m:
                param       = m.group(1).strip()
                value       = m.group(2).strip()
                paramname   = self._paramName(param)
                if paramname:
                    paramname   = paramname.lower()
                    self._header[paramname] = value
            else:
                self._header["simple_description"]    = l                
            

    def _paramName(self, param):
        """
        Returns parameter name.
        Note: Only those parameter which are in INFO_PARAMS will be returned
        """
        # Non standard parameter
        if self._isMatch(COPYRIGHT_N, param):
            return "copyright"

        # Standard parameters
        for regex in STD_PARAMS:
            if self._isMatch(regex, param):
                return param


        return None


    def _isMatch(self, regex, text):
        "Returns True if matches, False - otherwise"
        p       = re.compile(regex, re.IGNORECASE)
        m       = p.match(text)
        if m:
            return True # There is the match

        return False


    def _parseDescSection(self, text):
        "Parses description section and populates part of header parameters"
        # Find example
        p           = re.compile(EXAMPLE, re.DOTALL|re.IGNORECASE)
        matches     = p.findall(text)
        example     = ""        # Default value
        if len(matches) >= 1:   # No section found, return empty string
            mstr = matches[0]      # Take first match!
            if mstr:
                example  = " ".join(mstr.strip(" \n").split("\n"))

        self._header["example"]    = example


    def _parseParamSection(self, text):
        "Parses parameter section and populates input and output parameters of header"
        pass



testtext = """
/*******************************************************************************
*
*
*
* McStas, neutron ray-tracing package
*         Copyright 1997-2002, All rights reserved
*         Risoe National Laboratory, Roskilde, Denmark
*         Institut Laue Langevin, Grenoble, France
*
* Component: E_monitor
*
* %I
* Written by: Kristian Nielsen and Kim Lefmann
* Date: April 20, 1998
* Version: $Revision: 438 $
* Origin: Risoe
* Release: McStas 1.6
*
* Energy-sensitive monitor.
*
* %D
* A square single monitor that measures the energy of the incoming neutrons.
*
* Example: E_monitor(xmin=-0.1, xmax=0.1, ymin=-0.1, ymax=0.1,
*                 Emin=1, Emax=50, nchan=20, filename="Output.nrj")
*
* %P
* INPUT PARAMETERS:
*
* xmin:     Lower x bound of detector opening (m)
* xmax:     Upper x bound of detector opening (m)
* ymin:     Lower y bound of detector opening (m)
* ymax:     Upper y bound of detector opening (m)
* Emin:     Minimum energy to detect (meV)
* Emax:     Maximum energy to detect (meV)
* nchan:    Number of energy channels (1)
* filename: Name of file in which to store the detector image (text)
*
* OUTPUT PARAMETERS:
*
* E_N:      Array of neutron counts
* E_p:      Array of neutron weight counts
* E_p2:     Array of second moments
*
* %E
*******************************************************************************/
the rest of text
"""

if __name__ == "__main__":
    parser  = McStasComponentParser(config=testtext)
    print parser.toString()


__date__ = "$Sep 15, 2010 3:05:52 PM$"

