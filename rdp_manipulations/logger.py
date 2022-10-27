import sys
from loguru import logger as _logger
from rdp_manipulations.settings import LOG_LEVEL

_logger.remove()
_logger.add(sys.stderr, level=LOG_LEVEL)
_logger.debug('📝 Logger init')

logger = _logger
