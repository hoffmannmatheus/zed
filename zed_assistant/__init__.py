from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("zed-assistant")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0-local"

__all__ = [
    "__version__",
]
