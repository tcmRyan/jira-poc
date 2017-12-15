import requests

from server.authentication import AtlassianRequest
from server.models import Authentication


class AtLib:
    def __init__(self, domain):
        self.session = requests.Session()
        self.session.tenant_info = Authentication.query.filter_by(baseUrl=domain).first()

    # ============ Workflows ===========
    @property
    def workflows(self):
        rel = '/rest/api/2/workflow'
        return AtlassianRequest(self.session).get(rel).json()

    def get_workflow_schema(self, schema_id):
        rel = f'/rest/api/2/workflowscheme/{schema_id}'
        return AtlassianRequest(self.session).get(rel).json()

    # =============== Projects =======================
    @property
    def projects(self):
        rel = '/rest/api/2/project'
        return AtlassianRequest(self.session).get(rel).json()

    def get_properties_keys(self, project_id):
        rel = f'/rest/api/2/project/{project_id}/properties'
        return AtlassianRequest(self.session).get(rel).json()

    def explore_endpoint(self, method, rel, **kwargs):
        return AtlassianRequest(self.session).request(method, rel, **kwargs).json()
