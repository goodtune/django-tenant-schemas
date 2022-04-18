from django.contrib.staticfiles.storage import staticfiles_storage

from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.utils import get_tenant_model


class TenantStorageTests(TenantTestCase):
    def test_tenant(self):
        TenantModel = get_tenant_model()
        self.assertQuerysetEqual(
            TenantModel.objects.order_by("schema_name"),
            ["<Client: test>"],
        )
