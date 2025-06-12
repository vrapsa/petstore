from environs import Env

env = Env()
try:
    env.read_env()
except FileNotFoundError:
    pass

URL = env.str("URL", default="")
USER_ID = env.str("USER_ID", default="")
USERNAME = env.str("USERNAME", default="")
PASSWORD = env.str("PASSWORD", default="")
