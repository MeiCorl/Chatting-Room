from distutils.core import setup
import sys
import py2exe

# this allows to run it with a simple double click.
sys.argv.append('py2exe')

py2exe_options = {
    "includes": ["sip"],
    "dll_excludes": ["MSVCP90.dll", ],
    "compressed": 1,
    "optimize": 2,
    "ascii": 0,
    "bundle_files": 1,
}

setup(
    name='JJ',
    version='1.0',
    windows=['ChatClient.py', ],
    zipfile=None,
    options={'py2exe': py2exe_options}
)