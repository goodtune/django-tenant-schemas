from tenant_schemas.storage import TenantStaticFilesStorage
from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.utils import get_tenant_model, tenant_context


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

    def test_public_static_storage(self):
        TenantModel = get_tenant_model()
        tenant = TenantModel(schema_name="public", domain_url="public.test.com")
        with tenant_context(tenant):
            storage = TenantStaticFilesStorage()
            _, files = storage.listdir(".")
            with self.subTest(tenant=tenant):
                self.assertCountEqual(files, ["foo.txt", "bar.txt"])
            for filename in files:
                with self.subTest(filename=filename), storage.open(
                    "foo.txt", "rt"
                ) as fp:
                    self.assertEqual(fp.read(), "public")

    def test_tenant_static_storage(self):
        storage = TenantStaticFilesStorage()
        _, files = storage.listdir(".")
        with self.subTest(tenant=self.tenant):
            self.assertCountEqual(files, ["foo.txt", "baz.txt"])
        for filename in files:
            with self.subTest(filename=filename), storage.open("foo.txt", "rt") as fp:
                self.assertEqual(fp.read(), "tenant")
