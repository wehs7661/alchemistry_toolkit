"""
Unit and regression test for the alchemistry_toolkit package.
"""

# Import package, test suite, and other packages as needed
import alchemistry_toolkit
import pytest
import sys

def test_alchemistry_toolkit_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "alchemistry_toolkit" in sys.modules
