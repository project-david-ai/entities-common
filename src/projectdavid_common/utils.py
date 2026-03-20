# src/projectdavid_common/utilities.py
from projectdavid_common.utilities.identifier_service import IdentifierService
from projectdavid_common.utilities.logging_service import LoggingUtility
from projectdavid_common.utilities.tool_validator import ToolValidator


class UtilsInterface:
    """
    Provides access to utility services and helpers used across the system.

    Includes:
      - IdentifierService: for generating unique IDs.
      - LoggingUtility: for structured application logging.
      - load_environment: for loading environment variables based on runtime context.
    """

    IdentifierService = IdentifierService
    LoggingUtility = LoggingUtility
    ToolValidator = ToolValidator
