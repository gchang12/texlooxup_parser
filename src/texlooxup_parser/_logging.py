"""
"""

import logging

logger = logging.getLogger("texlooxup_parser")
logging.basicConfig(
    level=logging.DEBUG,
    filename="texlooxup_parser.log",
    filemode="w",
    format="%(levelname)s:%(name)s:%(funcName)s: %(message)s",
)
