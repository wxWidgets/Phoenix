

# Just a little convenience function that can be used by other build scripts
# or whatever to get the complete current version number.
def printVersion():
    from . import config
    oldval = config.runSilently
    config.runSilently = True
    cfg = config.Config(True)
    config.runSilently = oldval
    print(cfg.VERSION)
