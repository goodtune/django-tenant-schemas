from django.contrib.staticfiles.finders import BaseStorageFinder
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import connection


class TenantStaticStorageFinder(BaseStorageFinder):
    storage = staticfiles_storage

    def list(self, ignore_patterns):
        if connection.tenant and not isinstance(connection.tenant, FakeTenant):
            try:
                static_dirs = settings.MULTITENANT_STATIC_DIRS
            except AttributeError:
                raise ImproperlyConfigured(
                    "To use %s.%s you must define the MULTITENANT_STATIC_DIRS"
                    % (__name__, TenantStaticStorageFinder.__name__)
                )

            for static_dir in reversed(static_dirs):
                static_dir % (connection.tenant.domain_url,)
