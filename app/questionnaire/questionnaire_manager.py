class QuestionnaireManager(object):
    def __init__(self,
                 objectModel,        # Object Model
                 responseStore,      # ResponseStore instance
                 validationStore,    # ValidationStore instance
                 validator,          # ValidationEngine
                 router,             # RoutingEngine instance
                 navigator,          # Navigation instance
                 navigationHistory,  # NavigationHistory object
                 ):
        raise NotImplementedError()

    def process_incoming_response(self):
        raise NotImplementedError()

    def get_rendering_context(self):
        raise NotImplementedError()
