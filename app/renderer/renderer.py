from .rendering_context import RenderingContext


class Renderer(object):

    def render(self, model):
        return RenderingContext(model)
