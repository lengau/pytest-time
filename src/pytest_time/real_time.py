"""A copy of the real time module without any monkeypatching."""

# We're intentionally doing this to replicate the builtin time module.
from time import *  # noqa: F403 # pyright: ignore[reportWildcardImportFromLibrary]
