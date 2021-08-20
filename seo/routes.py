"""
Routes module.

Responsible for providing the means to register the application routes.
"""

from seo.controllers.health_api import HealthApiController
# from seo.controllers.example_api import ExampleApiController
from seo.controllers.meta_tags_api import MetaTagsApiController


def setup_routes(app):
    ###
    # Register the HelloWorld API handlers
    #

    health_api = HealthApiController()
    # example_api = ExampleApiController()
    meta_tags_api = MetaTagsApiController()

    ###
    # API v1.0 ROUTES
    #
    # Add your public v1.0 API routes here
    #
    # app.router.add_get('/api/v1.0/examples', example_api.get)
    # app.router.add_get('/api/v1.0/examples/{id}', example_api.get_by_id)

    # MetaTags
    app.router.add_post('/api/v1.0/meta_tags/', meta_tags_api.create)
    app.router.add_get('/api/v1.0/meta_tags/', meta_tags_api.get)
    app.router.add_get('/api/v1.0/meta_tags_slug/', meta_tags_api.get_by_slug)

    ###
    # INTERNAL API ROUTES
    #
    # Add your internal/administrative API routes here
    #
    app.router.add_get('/api/-/health', health_api.get)

