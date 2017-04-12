def setup_newrelic():
    import newrelic.agent
    newrelic.agent.initialize()
