"""
End-to-end tests for complete user workflows using external scripts.

This file now serves as a central hub for comprehensive workflow tests.
Individual test categories have been split into focused files:
- test_core_workflows.py: Basic metadata editing workflows
- test_format_specific_workflows.py: MP3/FLAC/WAV specific tests
- test_error_handling_workflows.py: Error scenarios and recovery
- test_rating_workflows.py: Rating normalization tests

This refactored version uses external scripts to set up test data
instead of the app's update functions, preventing circular dependencies.

These tests verify that the entire system works as expected for real users,
including file I/O, error handling, and complete metadata editing workflows.
"""