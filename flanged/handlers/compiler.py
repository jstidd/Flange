import falcon
import json

from flange import compiler

from flanged.handlers.base import _BaseHandler
from flanged.handlers.utils import get_body

class CompileHandler(_BaseHandler):
    def __init__(self, conf, db, rt):
        self.rt = rt
        super().__init__(conf, db)
    
    @falcon.before(_BaseHandler.do_auth)
    @falcon.after(_BaseHandler.encode_response)
    @get_body
    def on_post(self, req, resp, body):
        if "program" not in body:
            raise falcon.HTTPInvalidParam("Compilation request requires a program field", "program")
        ty = body.get("flags", {}).get("type", "netpath")
        
        try:
            resp.body = self.compute(body["program"], ty)
            resp.status = falcon.HTTP_200
        except falcon.HTTPUnprocessableEntity as exp:
            resp.body = { "error": str(exp) }
            resp.status = falcon.HTTP_500
        
    def authorize(self, attrs):
        return True if "x" in attrs else False
        
    def compute(self, prog, ty="netpath"):
        try:
            result = compiler.flange(prog, ty, self.rt)
        except Exception as exp:
            raise falcon.HTTPUnprocessableEntity(exp)
            
        self._db.insert(self._usr, prog)
        return result
