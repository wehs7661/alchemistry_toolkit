"""
Unit and regression test for the alchemistry_toolkit package.
"""

# Import package, test suite, and other packages as needed
import alchemistry_toolkit
import pytest
import sys
from alchemistry_toolkit import canvas

def test_alchemistry_toolkit_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "alchemistry_toolkit" in sys.modules

def test_alchemistry_toolkit_canvas():
    msg_1 = "The code is but a canvas to our imagination."
    msg_2 = msg_1 + "\n\t- Adapted from Henry David Thoreau"
    assert canvas(False) == msg_1
    assert canvas() == msg_2
