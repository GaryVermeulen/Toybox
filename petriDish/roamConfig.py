# roam_config.py
#
# Central config for cell roaming across hosts. Edit HOSTS to add, remove,
# or rename machines cells can roam to -- nothing else needs to change.
#
# This file gets copied to every host along with the rest of the project,
# so every host should have the SAME copy of it.

HOSTS = {
    "P3-Tiny": "10.0.0.50",
    "u1": "10.0.0.20",
    "u2": "10.0.0.30",
}

#HOSTS = {"P3-Tiny": "10.0.0.50"}

# Which host (by name, as listed above) runs the spawn coordinator service
# -- the tiny service that tracks total population and hands out cell IDs.
# Start spawnCoordinator.py on THIS host before starting cell1Body.py anywhere.
COORDINATOR_HOST = "P3-Tiny"
COORDINATOR_PORT = 5000
COORDINATOR_URL = "http://{}:{}".format(HOSTS[COORDINATOR_HOST], COORDINATOR_PORT)

# SSH user for remote launch (assumes passwordless key auth is already set
# up between every host in HOSTS).
SSH_USER = "gary"

# Absolute path to the Petri dish directory (the one containing cell*Body.py,
# cell*DNA.py, the data/ folder, txt/, etc.) -- must be the SAME path on
# every host in HOSTS, including the data/ folder's contents.
REMOTE_BASE_PATH = "/home/gary/bigO/petriDish"

# How long (seconds) a cell can go without a heartbeat before the
# coordinator assumes it died without checking out, and frees its
# population slot. Should be a few multiples of dna.sleepTime.
HEARTBEAT_TIMEOUT = 60

# Maximum population of children
MAXPOP = 5

