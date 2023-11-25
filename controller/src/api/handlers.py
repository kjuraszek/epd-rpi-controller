"""Module export request handlers for API"""

import io
import tornado.web
from PIL import Image

from src.view_manager import ViewManager
from .models import (
    StatusModel,
    CurrentDisplayModel,
)  # pylint: disable=W0611 # noqa: F401


class BaseHandler(tornado.web.RequestHandler):  # pylint: disable=W0223
    """Basic request handler upon which sets others should be based"""

    def set_default_headers(self) -> None:
        """Method sets necessary headers"""
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", " GET")
        return super().set_default_headers()


class RootHandler(BaseHandler):  # pylint: disable=W0223
    """Request handler for server's root folder"""

    def get(self) -> None:
        """Method handles GET request"""
        self.write("EPD RPI Controller's API root")


# pylint: disable=W0223,W0201
class StatusHandler(BaseHandler):
    """Request handler for status endpoint"""

    def initialize(self, view_manager: ViewManager) -> None:
        """Method initialises necessary properties"""
        self.view_manager = view_manager

    def get(self) -> None:
        """
        ---
        tags:
          - General
        summary: Get EPD status
        description: Get Epaper Display current status
        operationId: getStatus
        responses:
            200:
              description: EPD status
              schema:
                $ref: '#/definitions/StatusModel'
        """
        epd_status = self.view_manager.epd_status()
        self.write(epd_status)


# pylint: disable=W0223,W0201
class NextViewHandler(BaseHandler):
    """Request handler for endpoint which triggers the next view"""

    def initialize(self, view_manager: ViewManager) -> None:
        """Method initialises necessary properties"""
        self.view_manager = view_manager

    def get(self) -> None:
        """
        ---
        tags:
          - General
        summary: Next EPD view
        description: Switch EPD to the next one from views list
        operationId: nextView
        responses:
            '204':
              description: view change triggered
            '400':
              description: view change failed, epd is busy
        """
        if self.view_manager.busy.is_set():
            self.set_status(400, "View change failed - EPD is busy.")
            return

        self.view_manager.next()
        self.set_status(204)


# pylint: disable=W0223,W0201
class PreviousViewHandler(BaseHandler):
    """Request handler for endpoint which triggers the previous view"""

    def initialize(self, view_manager: ViewManager) -> None:
        """Method initialises necessary properties"""
        self.view_manager = view_manager

    def get(self) -> None:
        """
        ---
        tags:
          - General
        summary: Previous EPD view
        description: Switch EPD to the previous one from views list
        operationId: previousView
        responses:
            '204':
              description: view change triggered
            '400':
              description: view change failed, epd is busy
        """
        if self.view_manager.busy.is_set():
            self.set_status(400, "View change failed - EPD is busy.")
            return
        self.view_manager.prev()
        self.set_status(204)


# pylint: disable=W0223,W0201
class CurrentDisplayHandler(BaseHandler):
    """Request handler for endpoint which returns current view as image"""

    def initialize(self, view_manager: ViewManager) -> None:
        """Method initialises necessary properties"""
        self.view_manager = view_manager

    def get(self) -> None:
        """
        ---
        tags:
          - General
        summary: Get current display as image
        description: Get current display as jpeg image
        operationId: getCurrentDisplay
        responses:
            200:
              description: Current display as image returned successfully
              schema:
                $ref: '#/definitions/CurrentDisplayModel'
            400:
              description: Returning current display as image failed
        """
        current_image = self.view_manager.current_display()
        view_details = self.view_manager.current_view_details()
        if not current_image or not isinstance(current_image, Image.Image):
            self.set_status(400, "Returning current display failed.")
            return
        current_angle = view_details.get("view_angle", 0)
        current_image = current_image.rotate(current_angle * -1)
        current_image_buffer = io.BytesIO()
        current_image.save(current_image_buffer, format="JPEG")
        current_image_bytes = current_image_buffer.getvalue()
        self.set_header("Content-type", "image/jpg")
        self.set_header("Content-length", len(current_image_bytes))
        self.write(current_image_bytes)
