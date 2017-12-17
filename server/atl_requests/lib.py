import json
from server.atl_requests import AtlassianRequestor


class AtLib:
    def __init__(self, ctx):
        self.requestor = AtlassianRequestor(ctx)

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

    def get_issue_metadata(self):
        rel = '/rest/api/2/issue/createmeta'
        params = {'expand': 'projects'}
        return self.requestor.get(rel, params=params).json()

    def issue_changelog(self, issue_id):
        rel = f'/rest/api/2/issue/{issue_id}/changelog'
        return self.requestor.get(rel).json()

    def search(self, jql, start=0, max_results=50):
        is_last = False
        rel = '/rest/api/2/search'
        params = {
            'jql': jql,
            'startAt': start,
            'maxResults': max_results
        }
        while not is_last:
            resp = self.requestor.get(rel, params=params).json()
            if resp.get('isLast') or not resp.get('values'):
                is_last = True
            yield resp

    def get_transitions(self, issue_id_or_key):
        rel = f'/rest/api/2/issue/{issue_id_or_key}/transitions'
        params = {
            'expand': 'transitions.fields'
        }
        return self.requestor.get(rel, params=params).json()

    def do_transition(self, issue_id_or_key, data):
        rel = f'/rest/api/2/issue/{issue_id_or_key}/transitions'
        headers = {'Content-Type': 'application/json'}
        return self.requestor.post(rel, headers=headers, data=json.dumps(data))