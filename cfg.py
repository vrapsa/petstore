from environs import Env

env = Env()
try:
    env.read_env()
except FileNotFoundError:
    pass

URL = env.str("URL", default="")
USER_ID = env.str("USER_ID", default="")
USER_NAME = env.str("USER_NAME", default="")
USER_PASSWORD = env.str("USER_PASSWORD", default="")
