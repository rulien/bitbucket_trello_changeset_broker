import urllib
from brokers import BaseBroker
from django.utils import simplejson as sj

class URLOpener(urllib.FancyURLopener):
    version = 'bitbucket.org'
 
class DeployHQBroker(BaseBroker):
    
    """
    Three parameters are expected within the payload['service']:
    url (required) - the DeployHQ URL to which this broker will post
    notification_email (required) - the email to which DeployHQ will send deployment messages
    deploy_branch (optional) - the branch from which DeployHQ will deploy - defaults to 'master'

    Three parameters are expected within the payload['repository']:
    owner (required) - the owner of the repository
    slug (required) - the name of the repository
    scm (optional) - used to determine if a git or hg url should be sent to DeployHQ

    At least one parameter must be in the payload['commits']:
    raw_node or node if raw_node not available (required) - the commit ID for git or hg which DeployHQ will checkout and deploy
    """
    def handle(self, payload):

        #the DeployHQ URL to which this broker will post
        url = payload['service']['url']

        #the email to which DeployHQ will send deployment message
        notification_email = payload['service']['notification_email']

        #the branch from which DeployHQ will deploy - defaults to 'master'
        deploy_branch = payload['service']['deploy_branch'] if 'deploy_branch' in payload['service'] else 'master'
        
        #Construct the clone URL in this pattern for git: 
        # "git@bitbucket.org:accountname/reponame.git"
        # use this pattern for hg:
        # "ssh://hg@bitbucket.org/accountname/reponame/"
        if 'scm' in payload['repository'] and payload['repository']['scm'] == 'git':
            clone_url = "git@bitbucket.org:%s/%s.git" % (payload['repository']['owner'], payload['repository']['slug'])
        else:
            clone_url = "ssh://hg@bitbucket.org/%s/%s/" % (payload['repository']['owner'], payload['repository']['slug'])


        #commit ID - try the full raw_node value if it exists, else use the abreviated node value
        commit = payload['commits']
        #if we're dealing with a list, always select last item in list
        if isinstance(commit, list):
            commit = commit[len(commit) - 1]

        commit_id = commit['raw_node'] if 'raw_node' in commit else commit['node']

        #prepay payload for POST
        deployhq_payload = {
                "branch":    deploy_branch,
                "clone_url": clone_url,
                "email":     notification_email,
                "new_ref":   commit_id,
        }
        post_load = { 'payload': sj.dumps(deployhq_payload) }
 
        #post payload to our URL
        opener = self.get_local('opener', URLOpener)
        opener.open(url, urllib.urlencode(post_load))