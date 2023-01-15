from tornado_swagger.model import register_swagger_model


@register_swagger_model
class StatusModel:  # pylint: disable=R0903
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
        timestamp:
            type: string
    """


@register_swagger_model
class CurrentDisplayModel:  # pylint: disable=R0903
    """
    ---
    type: string
    description: EPD current display model representation
    format: binary
    """
