from uuid import UUID

from jsonpickle import handlers


class UUIDHandler(handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.hex

    def restore(self, obj):
        return UUID(obj, version=4)
