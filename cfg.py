from environs import Env

env = Env()
try:
    env.read_env()
except FileNotFoundError:
    pass

URL = env.str("URL", default="")
