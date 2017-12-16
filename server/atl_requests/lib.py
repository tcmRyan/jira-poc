from server.atl_requests import AtlassianRequest


class AtLib:
    def __init__(self, ctx):
        self.requestor = AtlassianRequest(ctx)

    # ============ Workflows ===========
    @property
    def workflows(self):
        rel = '/rest/api/2/workflow'
        return self.requestor.get(rel).json()

    def get_workflow_schema(self, schema_id):
        rel = f'/rest/api/2/workflowscheme/{schema_id}'
        return self.requestor.get(rel).json()

    # =============== Projects =======================
    @property
    def projects(self):
        rel = '/rest/api/2/project'
        return self.requestor.get(rel).json()

    def get_properties_keys(self, project_id):
        rel = f'/rest/api/2/project/{project_id}/properties'
        return self.requestor.get(rel).json()

    def explore_endpoint(self, method, rel, **kwargs):
        return self.requestor.request(method, rel, **kwargs).json()