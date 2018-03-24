from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
 
 
 
class MyUserManager(BaseUserManager):
    use_in_migrations = True
    
    # python manage.py createsuperuser
    def create_superuser(self, sid, is_staff, password):
        user = self.model(
                          sid = sid,                         
                          is_staff = is_staff,
                          is_admin=True
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user
 
class UserModel(AbstractBaseUser):
    sid = models.CharField(verbose_name='ID',max_length=255,unique=True,primary_key=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    
 
 
    objects = MyUserManager()
 
    USERNAME_FIELD = "sid"
    # REQUIRED_FIELDS must contain all required fields on your User model, 
    # but should not contain the USERNAME_FIELD or password as these fields will always be prompted for.
    REQUIRED_FIELDS = ['is_staff']
 
    class Meta:
        app_label = "login"
        db_table = "users"
 
    def __str__(self):
        return self.sid
 
    def get_full_name(self):
        return self.sid
 
    def get_short_name(self):
        return self.sid
 
 
    # this methods are require to login super user from admin panel
    def has_perm(self, perm, obj=None):
        return self.is_admin
 
    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_admin
