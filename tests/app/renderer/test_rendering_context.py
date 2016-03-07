from app.renderer.rendering_context import RenderingContext
from app.model.questionnaire import Questionnaire

import unittest


class RenderingContextTests(unittest.TestCase):

    def test_get_model(self):
        model = Questionnaire()
        rendering_context = RenderingContext(model=model)
        self.assertEquals(model, rendering_context.get_model())


if __name__ == '__main__':
    unittest.main()

