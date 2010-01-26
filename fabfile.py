from fabric.api import local

def test():
    """
    Run tests for d51.django.apps.schedules
    """
    print local("python ./run_tests.py", capture=True)

def init():
    """
    Initialize a virtualenv in which to run tests against this
    """
    local("virtualenv .")
    local("pip install -E . -r requirements.txt")

def clean():
    """
    Remove the cruft created by virtualenv and pip
    """
    local("rm -rf bin/ include/ lib/")

