from tornado_swagger.model import register_swagger_model


@register_swagger_model
class StatusModel:
    """
    ---
    type: object
    description: EPD status model representation
    properties:
        current_view:
            type: integer
            format: int64
        epd_busy:
            type: boolean
        total_views:
            type: integer
            format: int64
    """
