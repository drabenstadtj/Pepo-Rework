import multiprocessing

# Use all available CPU cores for workers
workers = multiprocessing.cpu_count() * 2 + 1

# Bind to all interfaces on port 5000
bind = "0.0.0.0:5000"

# Log to stdout/stderr
loglevel = "info"
errorlog = "-"
accesslog = "-"
