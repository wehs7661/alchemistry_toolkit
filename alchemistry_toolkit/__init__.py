"""
alchemistry_toolkit
A toolkit of data analysis for alchemical calculations or relevant advanced sampling methods
"""

# Add imports here
from .alchemistry_toolkit import *
from .parsers import *
from .estimators import *
import alehcmistry_toolkit.utils

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
