import io
import tornado.web
from PIL import Image

from .models import StatusModel, CurrentDisplayModel


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("EPD RPI Controller's API root")


class StatusHandler(tornado.web.RequestHandler):
    def initialize(self, view_manager):
        self.view_manager = view_manager
    def get(self):
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


class NextViewHandler(tornado.web.RequestHandler):
    def initialize(self, view_manager):
        self.view_manager = view_manager
    def get(self):
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


class PreviousViewHandler(tornado.web.RequestHandler):
    def initialize(self, view_manager):
        self.view_manager = view_manager
    def get(self):
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


class CurrentDisplayHandler(tornado.web.RequestHandler):
    def initialize(self, view_manager):
        self.view_manager = view_manager
    def get(self):
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
        if not current_image or not isinstance(current_image, Image.Image):
            self.set_status(400, "Returning current display failed.")
            return
        bytes_io = io.BytesIO()
        current_image.save(bytes_io, format="JPEG")
        current_image_string = bytes_io.getvalue()
        self.set_header('Content-type', 'image/jpg')
        self.set_header('Content-length', len(current_image_string))   
        self.write(current_image_string)
