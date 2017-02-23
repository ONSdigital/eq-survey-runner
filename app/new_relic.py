from app import settings


def setup_newrelic():
    if settings.EQ_NEW_RELIC_ENABLED:
        import newrelic.agent
        newrelic.agent.initialize()
