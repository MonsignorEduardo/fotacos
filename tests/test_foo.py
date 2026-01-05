"""Test basic application imports."""


def test_import_main():
    """Test that main module can be imported without GUI dependencies."""
    from fotacos.main import cli, main

    assert cli is not None
    assert main is not None


def test_import_api():
    """Test that API module can be imported."""
    from fotacos.api import app

    assert app is not None
