#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
__version__ = "DEV-ALPHA 2.3.0"
__author__ = "Zach Rogers - PyOnline Development Team"

# Versioning scheme based on: http://en.wikipedia.org/wiki/Versioning#Designating_development_stage
#
#   +-- api change, probably incompatible with older versions
#   |     +-- enhancements but no api change
#   |     |
# major.minor[.build[.revision]]
#                |
#                +-|* 0 for alpha (status)
#                  |* 1 for beta (status)
#                  |* 2 for release candidate
#                  |* 3 for (public) release

#-------------------------------------------------------------------------------
#     _________________
# ___/ Module Imports  \________________________________________________________
#PyOnline
import Update
import Login
import Networking.Client


def Main():
    #Set the client version
    Networking.Client.CLIENT_VER = str(__version__)

    #Run Update Check
    #Update.Check()

    #Run the Login Window (takes care of starting the game)
    Login.Run()


#Call Main() at startup
Main()