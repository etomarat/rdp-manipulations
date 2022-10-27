import environs

env = environs.Env()
env.read_env()

LOG_LEVEL = env("LOG_LEVEL", 'INFO')

RDP_HOST = env("RDP_HOST")
RDP_PORT = env("RDP_PORT")
RPD_LOGIN = env("RPD_LOGIN")
RDP_PASSWORD = env("RDP_PASSWORD")
