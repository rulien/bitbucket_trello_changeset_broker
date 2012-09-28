import unittest
import json
from broker import DeployHQBroker

"""
Execute tests:
$ python tests.py


For debugging:
$ python -m pdb tests.py

"""
#class TestDeployHQ(): #Alternate class statement for interactive command line testing
class TestCommentTrelloCard(unittest.TestCase):

    def setUp(self):
		self.apiKey = "e83104e0d315c9fe338cc02b91333153"
        self.commentChangeSetTrello = """
        {
            "broker": "trello", 
            "commits": [
                {
                    "author": "knutmc", 
                    "files": [
                        {
                            "file": "Classes/Pages/Keno/KenoDrawResultVC.xib", 
                            "type": "modified"
                        }, 
                        {
                            "file": "Classes/Pages/UIComponents/CountDown/CountDownAndNotificationView~iphone.xib", 
                            "type": "modified"
                        }, 
                        {
                            "file": "Classes/Pages/UIComponents/Trekningstall/Kulespill/Andre_tallspill/KenoDrawnNumbersView~iphone.xib", 
                            "type": "modified"
                        }
                    ], 
                    "message": "Jadda", 
                    "node": "f2187ed4fe86", 
                    "revision": 1650, 
                    "size": 684
                }
            ], 
            "repository": {
                "absolute_url": "/agens/bitbucket/", 
                "name": "bitbucket", 
                "owner": "agens", 
                "slug": "bitbucket", 
                "website": "http://bitbucket.org/"
            }, 
            "service": {"url": "http://www.trello.com/", "notification_email": "rulien79@gmail.com" }
        }
        """

        #Test with all required params and optional branch params
        self.deployhq_test_post1 = """
        {
            "service": {"url": "http://localhost:8000/post_dump", "notification_email": "testemail@gmail.com", "deploy_branch": "master" },
            "canon_url": "https://bitbucket.org", 
            "commits": [
                {
                    "author": "testuser", 
                    "branch": "master", 
                    "files": [
                        {
                            "file": "webapp/settings.py", 
                            "type": "modified"
                        }
                    ], 
                    "message": "test commit 2\\n", 
                    "node": "cd4fbbdce7f4", 
                    "parents": [
                        "afa01ed6c229"
                    ], 
                    "raw_author": "Test User <testemail@gmail.com>", 
                    "raw_node": "cd4fbbdce7f4e95284d552ad5868acc1cf42252c", 
                    "revision": null, 
                    "size": -1, 
                    "timestamp": "2012-03-20 06:01:44", 
                    "utctimestamp": "2012-03-20 05:01:44+00:00"
                }
            ], 
            "repository": {
                "absolute_url": "/testuser/testrepo/", 
                "fork": false, 
                "is_private": true, 
                "name": "testrepo", 
                "owner": "testuser", 
                "scm": "git", 
                "slug": "testrepo", 
                "website": ""
            }, 
            "user": "testuser"
        }
        """

        # No branch param
        self.deployhq_test_post2 = """
        {
            "service": {"url": "http://localhost:8000/post_dump", "notification_email": "testemail@gmail.com" },
            "canon_url": "https://bitbucket.org", 
            "commits": [
                {
                    "author": "testuser", 
                    "branch": "master", 
                    "files": [
                        {
                            "file": "webapp/settings.py", 
                            "type": "modified"
                        }
                    ], 
                    "message": "test commit 2\\n", 
                    "node": "cd4fbbdce7f4", 
                    "parents": [
                        "afa01ed6c229"
                    ], 
                    "raw_author": "Test User <testemail@gmail.com>", 
                    "raw_node": "cd4fbbdce7f4e95284d552ad5868acc1cf42252c", 
                    "revision": null, 
                    "size": -1, 
                    "timestamp": "2012-03-20 06:01:44", 
                    "utctimestamp": "2012-03-20 05:01:44+00:00"
                },
                {
                    "author": "testuser", 
                    "branch": "master", 
                    "files": [
                        {
                            "file": "webapp/test.py", 
                            "type": "modified"
                        }
                    ], 
                    "message": "test commit 2\\n", 
                    "node": "123123123", 
                    "parents": [
                        "afa01ed6c229"
                    ], 
                    "raw_author": "Test User <testemail@gmail.com>", 
                    "raw_node": "123123123", 
                    "revision": null, 
                    "size": -1, 
                    "timestamp": "2012-03-21 06:01:44", 
                    "utctimestamp": "2012-03-21 05:01:44+00:00"
                }
            ], 
            "repository": {
                "absolute_url": "/testuser/testrepo/", 
                "fork": false, 
                "is_private": true, 
                "name": "testrepo", 
                "owner": "testuser", 
                "scm": "git", 
                "slug": "testrepo", 
                "website": ""
            }, 
            "user": "testuser"
        }
        """

        #Commits is a dict instead of list
        self.deployhq_test_post3 = """
        {
            "service": {"url": "http://localhost:8000/post_dump", "notification_email": "testemail@gmail.com", "deploy_branch": "master" },
            "canon_url": "https://bitbucket.org", 
            "commits": 
                {
                    "author": "testuser", 
                    "branch": "master", 
                    "files": [
                        {
                            "file": "webapp/settings.py", 
                            "type": "modified"
                        }
                    ], 
                    "message": "test commit 2\\n", 
                    "node": "cd4fbbdce7f4", 
                    "parents": [
                        "afa01ed6c229"
                    ], 
                    "raw_author": "Test User <testemail@gmail.com>", 
                    "raw_node": "cd4fbbdce7f4e95284d552ad5868acc1cf42252c", 
                    "revision": null, 
                    "size": -1, 
                    "timestamp": "2012-03-20 06:01:44", 
                    "utctimestamp": "2012-03-20 05:01:44+00:00"
                }
            , 
            "repository": {
                "absolute_url": "/testuser/testrepo/", 
                "fork": false, 
                "is_private": true, 
                "name": "testrepo", 
                "owner": "testuser", 
                "scm": "git", 
                "slug": "testrepo", 
                "website": ""
            }, 
            "user": "testuser"
        }
        """


    def test_posts(self):

        broker = DeployHQBroker()
        
        #broker.handle(json.loads(self.deployhq_actual))
        
        broker.handle(json.loads(self.commentChangeSetTrello))

       # broker.handle(json.loads(self.deployhq_test_post1))
        
       # broker.handle(json.loads(self.deployhq_test_post2))

        #broker.handle(json.loads(self.deployhq_test_post3))

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()