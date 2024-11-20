import logging

def setup_logger():
    """
    Configures the logging settings for the application.

    Returns:
        Logger: Configured logger instance.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()
