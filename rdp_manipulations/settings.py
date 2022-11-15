import environs

env = environs.Env()
env.read_env()

LOG_LEVEL = env("LOG_LEVEL", 'INFO')
