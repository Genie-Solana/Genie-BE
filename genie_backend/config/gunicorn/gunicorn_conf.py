import multiprocessing

from psycogreen.gevent import patch_psycopg

name = "genie_backend"
bind = "tcp://localhost:8000"
workers = multiprocessing.cpu_count() * 2 + 1
keepalive = 32
worker_connections = 1000 * workers
worker_class = "gevent"
reload = True
loglevel = "info"
logfile = "-"
spew = False
max_requests = 5000
max_requests_jitter = 60
graceful_timeout = 120
timeout = 120
BASE_DIR = "/app/genie_backend"
pythonpath = BASE_DIR
chdir = BASE_DIR

# memory issue solver
# preload_app = False


def pre_fork(_, worker):
    from gevent import monkey

    patch_psycopg()
    worker.log.info("Made PostgreSQL Green!")
    monkey.patch_all()