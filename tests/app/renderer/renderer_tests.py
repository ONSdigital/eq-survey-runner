from app.renderer.renderer import Renderer
from app.renderer.rendering_context import RenderingContext

import unittest


class RendererTests(unittest.TestCase):

    def test_render(self):
        renderer = Renderer()
        self.assertIsInstance(renderer.render(model=None), RenderingContext)

if __name__ == '__main__':
    unittest.main()
