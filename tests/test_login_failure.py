import pytest
from pytest_bdd import scenario, given, when, then

# Import steps so they are registered
from features.steps.login_steps import *


@scenario('../features/login.feature', 'Failed login with invalid credentials')
def test_failed_login():
    """Test for failed login with invalid credentials."""
    pass 