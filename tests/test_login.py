import pytest
from pytest_bdd import scenario, given, when, then

# Import steps so they are registered
from features.steps.login_steps import *


@scenario('../features/login.feature', 'Successful login with valid credentials')
def test_successful_login():
    """Test for successful login with valid credentials."""
    pass 