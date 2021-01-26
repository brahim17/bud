import confuse as cf


def configure():
    config = cf.Configuration('bud', __name__)
    config.set_file('./config.yaml')

    return config


def get_path():
    cfg = configure()
    return str(cfg["directory_path"])
