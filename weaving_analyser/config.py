import logging

# Create separate loggers for debug and warning levels
debug_logger = logging.getLogger('debug_logger')
warning_logger = logging.getLogger('warning_logger')
info_logger = logging.getLogger('info_logger')
console_logger = logging.getLogger('console_logger')
error_logger = logging.getLogger('error_logger')

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

# Configure the info logger
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler('logs/surface_inspection_info.log')
info_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
info_handler.setFormatter(info_formatter)
info_logger.addHandler(info_handler)

# Configure the console logger
console_logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
console_logger.addHandler(console_handler)

# Configure the error logger
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler('logs/surface_inspection_error.log')
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

