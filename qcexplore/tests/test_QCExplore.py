"""
Unit and regression test for the QCExplore package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import QCExplore


def test_QCExplore_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "QCExplore" in sys.modules
