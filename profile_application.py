#!/usr/bin/env python
import os
from werkzeug.middleware.profiler import ProfilerMiddleware

from app.setup import create_app  # NOQA


def setup_profiling(application):

    profiling_dir = 'profiling'

    if not os.path.exists(profiling_dir):
        os.makedirs(profiling_dir)

    application.wsgi_app = ProfilerMiddleware(
        application.wsgi_app, profile_dir=profiling_dir
    )
    application.debug = True


app = create_app({'PROFILE': True})
setup_profiling(app)
app.run(debug=True)
