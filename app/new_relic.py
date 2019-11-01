def setup_newrelic():
    import newrelic.agent  # pylint: disable=import-outside-toplevel

    newrelic.agent.initialize()
