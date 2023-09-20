import logging

# Create separate loggers for debug and warning levels
debug_logger = logging.getLogger('debug_logger')
warning_logger = logging.getLogger('warning_logger')

# Configure the debug logger
debug_logger.setLevel(logging.DEBUG)
debug_handler = logging.FileHandler('logs/surface_inspection_debug.log')
debug_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
debug_handler.setFormatter(debug_formatter)
debug_logger.addHandler(debug_handler)

# Configure the warning logger
warning_logger.setLevel(logging.WARNING)
warning_handler = logging.FileHandler('logs/surface_inspection_warning.log')
warning_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
warning_handler.setFormatter(warning_formatter)
warning_logger.addHandler(warning_handler)