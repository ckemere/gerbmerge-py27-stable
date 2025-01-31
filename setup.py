#!/usr/bin/env python
import sys
import glob
import os

from setuptools import setup, Extension
import distutils.sysconfig

from gerbmerge.__version_info__ import __version__

if sys.version_info < (2,4,0):
  print '*'*73
  print 'GerbMerge version %d.%d requires Python 2.4 or higher' % (VERSION_MAJOR, VERSION_MINOR)
  print '*'*73
  sys.exit(1)

if 0:
  for key,val in distutils.sysconfig.get_config_vars().items():
    print key
    print '***********************'
    print '  ', val
    print
    print

  sys.exit(0)

SampleFiles = glob.glob('testdata/*')
DocFiles = glob.glob('doc/*')
AuxFiles = ['LICENSE']

if sys.platform == 'win32' or ('bdist_wininst' in sys.argv):
  #DestLib = distutils.sysconfig.get_config_var('prefix')
  #DestDir = os.path.join(DestLib, 'gerbmerge')
  #BinDir = DestLib
  DestLib = distutils.sysconfig.get_python_lib()
  DestDir = os.path.join(DestLib, 'gerbmerge')
  BinFiles = ['misc/gerbmerge.bat']
  BinDir = '.'
  
  # Create top-level invocation program
  if not os.path.exists('misc'):
    os.makedirs('misc')
  fid = file('misc/gerbmerge.bat', 'wt')
  fid.write( \
  r"""@echo off
%s %s\gerbmerge\gerbmerge.py %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9
  """ % (sys.executable, DestLib) )
  fid.close()

else:
  # try to find the library location on this platform
  DestLib = distutils.sysconfig.get_python_lib()
  DestDir = os.path.join(DestLib, 'gerbmerge')
  BinFiles = ['misc/gerbmerge']
  BinDir = distutils.sysconfig.get_config_var('BINDIR')  

  # Create top-level invocation program
  if not os.path.exists('misc'):
    os.makedirs('misc')
  fid = file('misc/gerbmerge', 'wt')
  fid.write( \
  r"""#!/bin/sh
python %s/gerbmerge/gerbmerge.py $*
  """ % DestLib)
  fid.close()

dist=setup (name = "gerbmerge",
       license = "GPL",
       version = __version__,
      long_description=\
r"""GerbMerge is a program that combines several Gerber
(i.e., RS274-X) and Excellon files into a single set
of files. This program is useful for combining multiple
printed circuit board layout files into a single job.

To run the program, invoke the Python interpreter on the
gerbmerge.py file. On Windows, if you installed GerbMerge in
C:/Python24, for example, open a command window (DOS box)
and type:
    C:/Python24/gerbmerge.bat

For more details on installation or running GerbMerge, see the
URL below.
""",
       description = "Merge multiple Gerber/Excellon files",
       author = "Unwired Devices LLC",
       author_email = "info@unwds.com",
       url = "https://github.com/unwireddevices/gerbmerge",
       packages = ['gerbmerge'],
       platforms = ['all'],
       data_files = [ (DestDir, AuxFiles), 
                      (os.path.join(DestDir,'testdata'), SampleFiles),
                      (os.path.join(DestDir,'doc'), DocFiles),
                      (BinDir, BinFiles) ],
       install_requires = ['simpleparse']
)

do_fix_perms = 0
if sys.platform != "win32":
  for cmd in dist.commands:
   if cmd[:7]=='install':
    do_fix_perms = 1
    break

if do_fix_perms:
  # Ensure package files and misc/help files are world readable-searchable.
  # Shouldn't Distutils do this for us?
  print 'Setting permissions on installed files...',
  try:
    def fixperms(arg, dirname, names):
      os.chmod(dirname, 0755)
      for name in names:
        fullname = os.path.join(dirname, name)
        if os.access(fullname, os.X_OK):
          os.chmod(fullname, 0755)
        else:
          os.chmod(fullname, 0644)

    os.path.walk(DestDir, fixperms, 1)
    os.path.walk(os.path.join(DestLib, 'site-packages/gerbmerge'), fixperms, 1)

    os.chmod(os.path.join(BinDir, 'gerbmerge'), 0755)
    print 'done'
  except:
    print 'FAILED'
    print
    print '*** Please verify that the installed files have correct permissions. On'
    print "*** systems without permission flags, you don't need to"
    print '*** worry about it.' 

if sys.platform != "win32":
  if cmd[:7]=='install':
    print
    print '******** Installation Complete ******** '
    print
    print 'Sample files and documentation have been installed in:'
    print '   ', DestDir
    print
    print 'A shortcut to starting the program has been installed as:'
    print '   ', os.path.join(BinDir, 'gerbmerge')
    print
