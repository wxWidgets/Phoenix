These two examples demonstrate a more advanced use of pubsub. One of the
examples uses the *kwargs* messaging protocol, the other uses the *arg1*
messaging protocol. There are two examples that can be run from this folder:

**main_kwargs.py**: advanced example that shows other capabilities of
    pubsub such as pubsub notification and listener exception 
    handling, in the 'kwargs' messaging protocol. All modules that
    start with 'kwargs\_' are used, as well as some modules that are
    independent of protocol and are shared with the arg1_main
    example.

**main_arg1.py**: same as kwargs_main but using the 'arg1' protocol.
    All modules that start with 'kwargs\_' are used, as well as some
    modules that are independent of protocol and are shared with the
    kwargs_main example.