"""Tests for {{PROJECT_NAME}}."""

import pytest
from {{PROJECT_SLUG}}.main import main


def test_main_function_exists():
    """Test that main function exists and is callable."""
    assert callable(main)


def test_main_runs_without_error():
    """Test that main runs without raising exceptions."""
    try:
        main()
    except Exception as e:
        pytest.fail(f"main() raised {e} unexpectedly")


def test_module_has_version():
    """Test that module has version information."""
    import {{PROJECT_SLUG}}
    assert hasattr({{PROJECT_SLUG}}, "__version__")
    assert isinstance({{PROJECT_SLUG}}.__version__, str)
