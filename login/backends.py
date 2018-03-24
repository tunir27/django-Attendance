from login.models import UserModel
import logging
 
 
class MyAuthBackend(object):
    def authenticate(self, sid, password):    
        try:
            user = UserModel.objects.get(sid=sid)
            if user.check_password(password):
                return user
            else:
                return None
        except UserModel.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists " % sid)
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None
 
    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(sid=user_id)
            if user.is_active:
                return user
            return None
        except UserModel.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None
