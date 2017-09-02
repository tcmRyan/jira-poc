from server.authentication import AtlassianRequest
from server.models import Authentication


class AtLib(object):

    def __init__(self, domain):
        tenant_info = Authentication.query.filter_by(baseUrl=domain).first()
        self.tenant_info = tenant_info
        self.request = AtlassianRequest(tenant_info)

    # ============ Workflows ===========
    @property
    def workflows(self):
        rel = '/rest/api/2/workflow'
        return self.request.request('GET', rel).json()

    def get_workflow_schema(self, schema_id):
        rel = '/rest/api/2/workflowscheme/{schema_id}'.format(schema_id=schema_id)
        return self.request.request('GET', rel).json()

    # =============== Projects =======================
    @property
    def projects(self):
        rel = '/rest/api/2/project'
        return self.request.request('GET', rel).json()

    def get_properties_keys(self, project_id):
        rel = '/rest/api/2/project/{project_id}/properties'.format(project_id=project_id)
        return self.request.request('GET', rel).json()

    def explore_endpoint(self, method, rel, **kwargs):
        return self.request.request(method, rel, **kwargs).json()
