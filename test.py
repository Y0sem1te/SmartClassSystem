import PyQt5
import matplotlib
import thop
import dlib
from packaging import version
required_version = version.parse("0.0.31-2005241907")
installed_version = version.parse(thop.__version__)
if installed_version < required_version:
    raise ImportError(f"thop version must be at least {required_version}, found {installed_version}")