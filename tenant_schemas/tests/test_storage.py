from django.contrib.staticfiles.storage import staticfiles_storage

from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.utils import get_tenant_model


class TenantStorageTests(TenantTestCase):
    """
    In our data folder, we have 4 files, path and content described as:

    -   public.test.com/foo.txt "public"
    -   public.test.com/bar.txt "public"
    -   tenant.test.com/foo.txt "tenant"
    -   tenant.test.com/baz.txt "tenant"

    We will define tests below will show that the finder approach is working
    correctly and that we can serve our files using standard techniques.
    """

    def test_tenant(self):
        TenantModel = get_tenant_model()
        self.assertQuerysetEqual(
            TenantModel.objects.order_by("schema_name"),
            ["<Tenant: test>"],
        )
