import json

from lfmcli.controller import Controller

OFNODE_CONN_STATS = \
    'opendaylight-port-statistics:flow-capable-node-connector-statistics'


class FlowManagerClientException(Exception):
    """Flow Manager Client Exception class"""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Client():
    """Class that represents a Flowmanager service """

    def __init__(self, **kwargs):
        """Initializes this object properties."""
        self.ctrl = Controller(**kwargs)

    def __str__(self):
        """ Returns string representation of this object. """
        return str(vars(self))

    def to_string(self):
        """ Returns string representation of this object. """
        return self.__str__()

    def to_json(self):
        """ Returns JSON representation of this object. """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

    def brief_json(self):
        """ Returns JSON representation of this object (brief info). """
        d = {}
        return json.dumps(d, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)

    def get_paths(self, config=True):
        """ get paths from Flow Manager """
        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config)+"/lumina-flowmanager-path:paths")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200:
                r['paths'] = json.loads(resp.content)

        return r

    def get_path(self, name, config=True):
        """ Get a Flow Manager path given the path name

        :param name: path name to get
        :return: response keywords (see add_path for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config) +
                   "/lumina-flowmanager-path:paths/path/{}".format(name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                path = json.loads(resp.content).get('path')
                if path:
                    r['path'] = path[0]
                else:
                    r['path'] = None

        return r

    def add_path(self, **kwargs):
        """ Add or create a path via Flow Manager.

        :param path: Path keywords see below
        :return: returns a resp dict (See below)

        :Path Keywords:

        required:
          'name': 'name of this path'
          'endpoint1': source switch
          'endpoint2': destination switch

        optional:
          'provider': defaults to sr

        Response Dict:
          'status_cod': http response status code
          'content': http response content
          'paths': path keywords in API format

        """

        # Now translate from API to what Flow Manager needs
        path = kwargs.get('path')
        if not path:
            raise FlowManagerClientException('didn\'t get any path properties')

        # Make call to Flow Manager
        payload = {"path": [path]}
        resp = self.ctrl.http_put_request(
                 self.ctrl.get_config_url() +
                 "/lumina-flowmanager-path:paths/path/{}".format(path['name']),
                 json.dumps(payload))

        # Check response
        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if (resp.status_code == 200) or (resp.status_code == 201):
                r = self.get_path(path['name'])

        return r

    def delete_path(self, name):
        """ Delete a path via Flow Manager.

        :param name: name of path to delete
        :return: response keywords (see add_path for description)

        """

        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url() +
                   "/lumina-flowmanager-path:paths/path/{}".format(name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
        else:
            r = self.get_path(name)

        return r

    def delete_paths(self):
        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url()+"/lumina-flowmanager-path:paths")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
            else:
                r = self.get_paths()

        return r

    def get_treepaths(self, config=True):
        """ get treepaths from Flow Manager """
        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config) +
                   "/lumina-flowmanager-tree-path:treepaths")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200:
                r['treepaths'] = json.loads(resp.content)

        return r

    def get_treepath(self, name, config=True):
        """ Get a Flow Manager treepath given the path name

        :param name: treepath name to get
        :return: response keywords (see add_treepath for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config) +
                   "/lumina-flowmanager-tree-path:treepaths/treepath/{}".format(name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                treepath = json.loads(resp.content).get('treepath')
                if treepath:
                    r['treepath'] = treepath[0]
                else:
                    r['treepath'] = None

        return r

    def add_treepath(self, **kwargs):
        """ Add or create a treepath via Flow Manager.

        :param treepath: Tree Path keywords see below
        :return: returns a resp dict (See below)

        :Path Keywords:

        required:
          'name': 'name of this treepath'
          'root': root node dict
          'leaves': leaves dict

        optional:
          'provider': defaults to sr

        Response Dict:
          'status_code': http response status code
          'content': http response content
          'treepaths': treepath keywords in API format

        """

        # Now translate from API to what Flow Manager needs
        treepath = kwargs.get('treepath')
        if not treepath:
            raise FlowManagerClientException(
                    'didn\'t get any treepath properties')

        # Make call to Flow Manager
        payload = {"treepath": [treepath]}
        resp = self.ctrl.http_put_request(
                 self.ctrl.get_config_url() +
                 "/lumina-flowmanager-tree-path:treepaths/treepath/{}".format(
                    treepath['name']), json.dumps(payload))

        # Check response
        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if (resp.status_code == 200) or (resp.status_code == 201):
                r = self.get_treepath(treepath['name'])

        return r

    def delete_treepath(self, name):
        """ Delete a treepath via Flow Manager.

        :param name: name of treepath to delete
        :return: response keywords (see add_treepath for description)

        """

        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url() +
                   "/lumina-flowmanager-tree-path:treepaths/treepath/{}".format(name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
        else:
            r = self.get_treepath(name)

        return r

    def delete_treepaths(self):
        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url() +
                   "/lumina-flowmanager-tree-path:treepaths")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
            else:
                r = self.get_treepaths()

        return r

    def get_treepath_leaf(self, name, node, config=True):
        """ Get a Flow Manager treepath leaf

        :param name: treepath name to get
        :param node: leaf node to get
        :return: response keywords (see add_treepath for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config) +
                   "/lumina-flowmanager-tree-path:treepaths/treepath" +
                   "/{}/leaves/leaf/{}".format(name, node))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                leaf = json.loads(resp.content).get('leaf')
                if leaf:
                    r['leaf'] = leaf[0]
                else:
                    r['leaf'] = None

        return r

    def add_treepath_leaf(self, name, node, leaf):
        """ Add or create a treepath leaf via Flow Manager.

        :param name: Tree Path name
        :param node: Tree Path leaf node id
        :param leaf: Tree Path keywords see below
        :return: returns a resp dict (See below)

        :leaf Keywords:

        required:
          'node': <node>   - node id of this leaf
          'constraints':   - constraints for this leaf node
            'waypoint': [  - List of waypoints
                {
                    'order': <integer>,    - order of this waypoint
                    'nodeid': <node-id>    - node id of this waypoint
                }
            ]

        Response Dict:
          'status_code': http response status code
          'content': http response content
          'leaves': leaves keywords in API format

        """

        # Make call to Flow Manager
        payload = {"leaf": [leaf]}
        resp = self.ctrl.http_put_request(
                 self.ctrl.get_config_url() +
                 "/lumina-flowmanager-tree-path:treepaths/treepath" +
                 "/{}/leaves/leaf/{}".format(name, node), json.dumps(payload))

        # Check response
        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if (resp.status_code == 200) or (resp.status_code == 201):
                r = self.get_treepath_leaf(name, node)

        return r

    def delete_treepath_leaf(self, name, node):
        """ Delete a treepath leaf node via Flow Manager.

        :param name: name of treepath to delete
        :param node: Tree Path leaf node id
        :return: response keywords (see add_treepath for description)

        """

        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url() +
                   "/lumina-flowmanager-tree-path:treepaths/treepath" +
                   "/{}/leaves/lead/{}".format(name, node))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
        else:
            r = self.get_treepath_leaf(name, node)

        return r

    def get_elines(self, config=True):
        """ get elines from Flow Manager """
        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config)+"/lumina-flowmanager-eline:elines")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200:
                r['elines'] = json.loads(resp.content)

        return r

    def get_eline(self, name, config=True):
        """ Get a Flow Manager eline given the eline name

        :param name: eline name to get
        :return: response keywords (see add_eline for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config) +
                   "/lumina-flowmanager-eline:elines/eline/{}".format(name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                eline = json.loads(resp.content).get('eline')
                if eline:
                    r['eline'] = eline[0]
                else:
                    r['eline'] = None

        return r

    def get_eline_stats(self, name):
        """ Get a Flow Manager eline stats given the eline name

        :param name: eline name to get
        :return: response keywords

        """

        data = {
            "input": {
              "name": name
            }
        }

        resp = self.ctrl.http_post_request(
                   self.ctrl.get_operations_url() +
                   "/lumina-flowmanager-eline:get-stats",
                   json.dumps(data))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                output = json.loads(resp.content).get('output')
                if output:
                    r['output'] = output
                else:
                    r['output'] = {}

        return r

    def add_eline(self, **kwargs):
        """ Add or create a eline via Flow Manager.

        :param eline: Path keywords see below
        :return: returns a resp dict (See below)

        :Path Keywords:

        required:
          'name': 'name of this eline'
          'endpoint1': source switch
          'endpoint2': destination switch

        optional:
          'provider': defaults to sr

        Response Dict:
          'status_cod': http response status code
          'content': http response content
          'elines': eline keywords in API format

        """

        # Now translate from API to what Flow Manager needs
        eline = kwargs['eline']
        if not eline:
            raise FlowManagerClientException(
                    'didn\'t get any eline properties')

        # Make call to Flow Manager
        payload = {"eline": [eline]}
        resp = self.ctrl.http_put_request(
                 self.ctrl.get_config_url() +
                 "/lumina-flowmanager-eline:elines/eline/{}".format(eline['name']),
                 json.dumps(payload))

        # Check response
        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if (resp.status_code == 200) or (resp.status_code == 201):
                r = self.get_eline(eline['name'])

        return r

    def delete_eline(self, name):
        """ Delete a eline via Flow Manager.

        :param name: name of eline to delete
        :return: response keywords (see add_eline for description)

        """

        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url() +
                   "/lumina-flowmanager-eline:elines/eline/{}".format(name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
        else:
            r = self.get_eline(name)

        return r

    def delete_elines(self):
        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url()+"/lumina-flowmanager-eline:elines")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
            else:
                r = self.get_elines()

        return r

    def get_tap_url(self, eline, endpoint, config=True):
        '''get the base tap url'''
        return(self.ctrl.get_req_url(config) +
               "/lumina-flowmanager-eline:elines/eline/{}/{}/taps".format(
                    eline, endpoint))

    def get_taps(self, eline, endpoint=None, config=True):
        """ get taps from Flow Manager """

        # Grab the taps for an endpoint
        resp = self.ctrl.http_get_request(
                  self.get_tap_url(eline, endpoint, config))

        # Setup the return dict
        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200:
                r[endpoint] = json.loads(resp.content)

        return r

    def get_tap(self, eline, endpoint, path_name, config=True):
        """ Get a Flow Manager tap given the eline name and path-name

        :param eline: eline name to get
        :param endpoint: endpoint name to get
        :param path-name: path-name to get
        :return: response keywords (see add_tap for description)

        """

        resp = self.ctrl.http_get_request(
                   self.get_tap_url(eline, endpoint, config) +
                   "/tap/{}".format(path_name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                tap = json.loads(resp.content).get('lumina-flowmanager-eline-tap:tap')
                if tap:
                    r['tap'] = tap[0]
                else:
                    r['tap'] = None

        return r

    def add_tap(self, eline, endpoint, **kwargs):
        """ Add or create a tap via Flow Manager.

        :param eline: eline name to get
        :param endpoint: endpoint name to get
        :return: returns a resp dict (See below)

        :Path Keywords:

        required:
          'path-name': 'name of this eline'
          'egress': {
            'action': [
                    {
                        'order': 3,
                        'output-action': {
                            'output-node-connector': '1' -> output port
                        }
                    }
                ]
          }

        Response Dict:
          'status_cod': http response status code
          'content': http response content
          'taps': tap keywords in API format

        """

        # Now translate from API to what Flow Manager needs
        tap = kwargs['tap']
        if not tap:
            raise FlowManagerClientException('didn\'t get any tap properties')

        # Make call to Flow Manager
        payload = {"tap": [tap]}
        resp = self.ctrl.http_put_request(
                 self.get_tap_url(eline, endpoint) +
                 "/tap/{}".format(tap['path-name']),
                 json.dumps(payload))

        # Check response
        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if (resp.status_code == 200) or (resp.status_code == 201):
                r = self.get_tap(eline, endpoint, tap['path-name'])

        return r

    def delete_tap(self, eline, endpoint, path_name):
        """ Delete a tap via Flow Manager.

        :param eline: eline name
        :param endpoint: endpoint name
        :param path_name: path name of tap to delete
        :return: response keywords (see add_tap for description)

        """

        resp = self.ctrl.http_delete_request(
                   self.get_tap_url(eline, endpoint) +
                   "/tap/{}".format(path_name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
        else:
            r = self.get_tap(eline, endpoint, path_name)

        return r

    def delete_taps(self, eline, endpoint):
        """ Delete a taps via Flow Manager.

        :param eline: eline name
        :param endpoint: endpoint name
        :return: response keywords (see add_tap for description)
        """

        resp = self.ctrl.http_delete_request(
                   self.get_tap_url(eline, endpoint))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
            else:
                r = self.get_taps(eline, endpoint)

        return r

    def get_etrees(self, config=True):
        """ get etrees from Flow Manager """
        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config)+"/lumina-flowmanager-etree:etrees")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200:
                r['etrees'] = json.loads(resp.content)

        return r

    def get_etree(self, name, config=True):
        """ Get a Flow Manager etree given the etree name

        :param name: etree name to get
        :return: response keywords (see add_etree for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config) +
                   "/lumina-flowmanager-etree:etrees/etree/{}".format(name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                etree = json.loads(resp.content).get('etree')
                if etree:
                    r['etree'] = etree[0]
                else:
                    r['etree'] = None

        return r

    def get_etree_stats(self, name):
        """ Get a Flow Manager etree stats given the etree name

        :param name: etree name to get
        :return: response keywords

        """

        data = {
            "input": {
              "name": name
            }
        }

        resp = self.ctrl.http_post_request(
                   self.ctrl.get_operations_url() +
                   "/lumina-flowmanager-etree:get-stats",
                   json.dumps(data))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                output = json.loads(resp.content).get('output')
                if output:
                    r['output'] = output
                else:
                    r['output'] = {}

        return r

    def add_etree(self, **kwargs):
        """ Add or create a etree via Flow Manager.

        :param etree: etree keywords see below
        :return: returns a resp dict (See below)

        :Path Keywords:

        required:
          'name': 'name of this etree'
          'root': root switch
          'leafs': list of leaf switches

        optional:
          'provider': defaults to sr

        Response Dict:
          'status_cod': http response status code
          'content': http response content
          'etrees': etree keywords in API format

        """

        # Now translate from API to what Flow Manager needs
        etree = kwargs['etree']
        if not etree:
            raise FlowManagerClientException(
                    'didn\'t get any etree properties')

        # Make call to Flow Manager
        payload = {"etree": [etree]}
        resp = self.ctrl.http_put_request(
                 self.ctrl.get_config_url() +
                 "/lumina-flowmanager-etree:etrees/etree/{}".format(etree['name']),
                 json.dumps(payload))

        # Check response
        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if (resp.status_code == 200) or (resp.status_code == 201):
                r = self.get_etree(etree['name'])

        return r

    def delete_etree(self, name):
        """ Delete a etree via Flow Manager.

        :param name: name of etree to delete
        :return: response keywords (see add_etree for description)

        """

        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url() +
                   "/lumina-flowmanager-etree:etrees/etree/{}".format(name))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
        else:
            r = self.get_etree(name)

        return r

    def delete_etrees(self):
        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url()+"/lumina-flowmanager-etree:etrees")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
            else:
                r = self.get_etrees()

        return r

    def get_etree_leaf(self, etree_name, node, config=True):
        """ Get a Flow Manager etree leaf given the etree name

        :param etree_name: etree name to get
        :param node: etree lead to get
        :return: response keywords (see add_etree for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(config) +
                   "/lumina-flowmanager-etree:etrees/etree/{}/leaves/leaf/{}".format(
                       etree_name, node))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                leaf = json.loads(resp.content).get('leaf')
                if leaf:
                    r['leaf'] = leaf[0]
                else:
                    r['leaf'] = None

        return r

    def add_etree_leaf(self, etree_name, leaf):
        """ Add or create an etree leaf node via Flow Manager.

        :param etree-name: etree name
        :param leaf: leaf keywords see below
        :return: returns a resp dict (See below)

        :Leaf Keywords:

        required:
          'node': node id of this leaf
          'action': openflow action list for this leaf

        Response Dict:
          'status_code': http response status code
          'content': http response content
          'leaf': leaf keywords in API format

        """

        # Now translate from API to what Flow Manager needs
        if not etree_name:
            raise FlowManagerClientException('didn\'t get etree-name property')
        if not leaf:
            raise FlowManagerClientException('didn\'t get any leaf properties')

        # Make call to Flow Manager
        payload = {"leaf": [leaf]}
        resp = self.ctrl.http_put_request(
                 self.ctrl.get_config_url() +
                 "/lumina-flowmanager-etree:etrees/etree/{}/leaves/leaf/{}".format(
                    etree_name, leaf['node']), json.dumps(payload))

        # Check response
        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if (resp.status_code == 200) or (resp.status_code == 201):
                r = self.get_etree_leaf(etree_name, leaf['node'])

        return r

    def delete_etree_leaf(self, etree_name, node):
        """ Delete an etree leaf via Flow Manager.

        :param etree_name: name of etree to delete
        :param node: name of leaf to delete
        :return: response keywords

        """

        resp = self.ctrl.http_delete_request(
                   self.ctrl.get_config_url() +
                   "/lumina-flowmanager-etree:etrees/etree/{}/leaves/leaf/{}".format(
                    etree_name, node))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200 or resp.status_code == 404:
                return r
        else:
            r = self.get_etree_leaf(etree_name, node)

        return r

    def get_ofnode(self, node):
        """ Get a Flow Manager OF Node given the node id

        :param node: openflow node id
        :return: response keywords (see add_etree for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(False) +
                   "/opendaylight-inventory:nodes/node/{}".format(node))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                node = json.loads(resp.content).get('node')
                if node:
                    r['node'] = node[0]
                else:
                    r['node'] = None

        return r

    def get_ofnodes(self):
        """ Get All OF Nodes given the node id

        @return: response keywords

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(False) +
                   "/opendaylight-inventory:nodes")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                nodes = json.loads(resp.content).get('nodes')
                if nodes:
                    r['nodes'] = nodes['node']
                else:
                    r['nodes'] = []

        return r

    def get_ofnode_connector(self, node, conn_id):
        """ Get an OF Node connector given the node id and connector id.

        :param node: openflow node id
        :param conn_id: connector id
        :return: response keywords

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(False) +
                   "/opendaylight-inventory:nodes/node/{}".format(node) +
                   "/node-connector/{}".format(conn_id))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                connector = json.loads(resp.content).get('node-connector')
                if connector:
                    r['node-connector'] = connector[0]
                else:
                    r['node-connector'] = None

        return r

    def get_ofnode_connector_stats(self, node, conn_id):
        """ Get an OF Node connector's stats given the node id and
            connector id.

        :param node: openflow node id
        :param conn_id: connector id
        :return: response keywords (see add_etree for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_req_url(False) +
                   "/opendaylight-inventory:nodes/node/{}".format(node) +
                   "/node-connector/{}/flow-capable-node-connector-statistics".
                   format(conn_id))

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content
            if resp.status_code == 200:
                stats = json.loads(resp.content).get(OFNODE_CONN_STATS)
                if stats:
                    r['stats'] = stats
                else:
                    r['stats'] = None

        return r


    def get_controller_status(self):
        """ Delete a etree via Flow Manager.

        :param name: name of etree to delete
        :return: response keywords (see add_etree for description)

        """

        resp = self.ctrl.http_get_request(
                   self.ctrl.get_operational_url() +
                   "/lumina-controller-status:system-status")

        r = {}
        if resp is not None:
            r['status_code'] = resp.status_code
            r['content'] = resp.content

            if resp.status_code == 200:
                return r

        return r
