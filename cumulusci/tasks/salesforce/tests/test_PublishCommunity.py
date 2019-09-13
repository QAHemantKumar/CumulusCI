import responses
import unittest
from cumulusci.tasks.salesforce import PublishCommunity
from cumulusci.core.exceptions import SalesforceException
from .util import create_task


task_options = {"name": "Test Community"}
task_options_with_id = {"name": "Test Community", "communityid": "000000000000000000"}


class test_PublishCommunity(unittest.TestCase):
    @responses.activate
    def test_publishes_community(self):
        cc_task = create_task(PublishCommunity, task_options)
        communities_url = "{}/services/data/v46.0/connect/communities".format(
            cc_task.org_config.instance_url
        )
        community_publish_url = "{}/services/data/v46.0/connect/communities/{}/publish".format(
            cc_task.org_config.instance_url, task_options_with_id["communityid"]
        )

        responses.add(
            method=responses.GET,
            url=communities_url,
            status=200,
            json={
                "communities": [
                    {
                        "allowChatterAccessWithoutLogin": "false",
                        "allowMembersToFlag": "false",
                        "description": "This is a test community",
                        "id": "{}".format(task_options_with_id["communityid"]),
                        "invitations​Enabled": "false",
                        "knowledgeable​Enabled": "false",
                        "loginUrl": "https://mydomain.force.com/test/s/login",
                        "memberVisibilityEnabled": "true",
                        "name": "{}".format(task_options["name"]),
                        "nicknameDisplayEnabled": "false",
                        "privateMessagesEnabled": "false",
                        "reputationEnabled": "false",
                        "sendWelcomeEmail": "true",
                        "siteAsContainerEnabled": "true",
                        "siteUrl": "https://mydomain.force.com/test",
                        "status": "Live",
                        "templateName": "VF Template",
                        "url": "/services/data/v46.0/connect/communities/{}".format(
                            task_options_with_id["communityid"]
                        ),
                        "urlPathPrefix": "test",
                    }
                ],
                "total": "1",
            },
        )

        responses.add(
            method=responses.POST,
            url=community_publish_url,
            status=200,
            json={
                "id": "{}".format(task_options_with_id["communityid"]),
                "message": "We are publishing your changes now. You will receive an email confirmation when your changes are live.",
                "name": "{}".format(task_options["name"]),
                "url": "https://mydomain.force.com/test",
            },
        )

        cc_task()

        self.assertEqual(2, len(responses.calls))
        self.assertEqual(communities_url, responses.calls[0].request.url)
        self.assertEqual(community_publish_url, responses.calls[1].request.url)

    @responses.activate
    def test_publishes_community_with_id(self):
        cc_task = create_task(PublishCommunity, task_options_with_id)
        community_url = "{}/services/data/v46.0/connect/communities/{}".format(
            cc_task.org_config.instance_url, task_options_with_id["communityid"]
        )
        community_publish_url = "{}/services/data/v46.0/connect/communities/{}/publish".format(
            cc_task.org_config.instance_url, task_options_with_id["communityid"]
        )

        responses.add(
            method=responses.GET,
            url=community_url,
            status=200,
            json={
                "allowChatterAccessWithoutLogin": "false",
                "allowMembersToFlag": "false",
                "description": "This is a test community",
                "id": "{}".format(task_options_with_id["communityid"]),
                "invitationsEnabled": "false",
                "knowledgeableEnabled": "false",
                "loginUrl": "https://mydomain.force.com/test/s/login",
                "memberVisibilityEnabled": "true",
                "name": "{}".format(task_options["name"]),
                "nicknameDisplayEnabled": "false",
                "privateMessagesEnabled": "false",
                "reputationEnabled": "false",
                "sendWelcomeEmail": "true",
                "siteAsContainerEnabled": "true",
                "siteUrl": "https://mydomain.force.com/test",
                "status": "Live",
                "templateName": "VF Template",
                "url": "/services/data/v46.0/connect/communities/{}".format(
                    task_options_with_id["communityid"]
                ),
                "urlPathPrefix": "test",
            },
        )

        responses.add(
            method=responses.POST,
            url=community_publish_url,
            status=200,
            json={
                "id": "{}".format(task_options_with_id["communityid"]),
                "message": "We are publishing your changes now. You will receive an email confirmation when your changes are live.",
                "name": "{}".format(task_options_with_id["name"]),
                "url": "https://mydomain.force.com/test",
            },
        )

        cc_task()

        self.assertEqual(2, len(responses.calls))
        self.assertEqual(community_url, responses.calls[0].request.url)
        self.assertEqual(community_publish_url, responses.calls[1].request.url)

    @responses.activate
    def test_throws_exception_for_bad_name(self):
        cc_task = create_task(PublishCommunity, task_options)
        communities_url = "{}/services/data/v46.0/connect/communities".format(
            cc_task.org_config.instance_url
        )

        responses.add(
            method=responses.GET,
            url=communities_url,
            status=200,
            json={
                "communities": [
                    {
                        "allowChatterAccessWithoutLogin": "false",
                        "allowMembersToFlag": "false",
                        "description": "This is a test community",
                        "id": "{}".format(task_options_with_id["communityid"]),
                        "invitationsEnabled": "false",
                        "knowledgeableEnabled": "false",
                        "loginUrl": "https://mydomain.force.com/test/s/login",
                        "memberVisibilityEnabled": "true",
                        "name": "Not {}".format(task_options["name"]),
                        "nicknameDisplayEnabled": "false",
                        "privateMessagesEnabled": "false",
                        "reputationEnabled": "false",
                        "sendWelcomeEmail": "true",
                        "siteAsContainerEnabled": "true",
                        "siteUrl": "https://mydomain.force.com/test",
                        "status": "Live",
                        "templateName": "VF Template",
                        "url": "/services/data/v46.0/connect/communities/{}".format(
                            task_options_with_id["communityid"]
                        ),
                        "urlPathPrefix": "test",
                    }
                ],
                "total": "1",
            },
        )

        with self.assertRaises(SalesforceException):
            cc_task._run_task()

    @responses.activate
    def test_throws_exception_for_bad_id(self):
        cc_task = create_task(PublishCommunity, task_options_with_id)
        community_url = "{}/services/data/v46.0/connect/communities/{}".format(
            cc_task.org_config.instance_url, task_options_with_id["communityid"]
        )

        responses.add(
            method=responses.GET,
            url=community_url,
            status=404,
            json=[
                {
                    "errorCode": "NOT_FOUND",
                    "message": "The requested resource does not exist",
                }
            ],
        )

        with self.assertRaises(SalesforceException):
            cc_task._run_task()

    @responses.activate
    def test_throws_exeption_for_unmatched_id(self):
        cc_task = create_task(PublishCommunity, task_options_with_id)
        community_url = "{}/services/data/v46.0/connect/communities/{}".format(
            cc_task.org_config.instance_url, task_options_with_id["communityid"]
        )

        responses.add(
            method=responses.GET,
            url=community_url,
            status=200,
            json={
                "allowChatterAccessWithoutLogin": "false",
                "allowMembersToFlag": "false",
                "description": "This is a test community",
                "id": "{}".format(task_options_with_id["communityid"]),
                "invitationsEnabled": "false",
                "knowledgeableEnabled": "false",
                "loginUrl": "https://mydomain.force.com/test/s/login",
                "memberVisibilityEnabled": "true",
                "name": "Not {}".format(task_options["name"]),
                "nicknameDisplayEnabled": "false",
                "privateMessagesEnabled": "false",
                "reputationEnabled": "false",
                "sendWelcomeEmail": "true",
                "siteAsContainerEnabled": "true",
                "siteUrl": "https://mydomain.force.com/test",
                "status": "Live",
                "templateName": "VF Template",
                "url": "/services/data/v46.0/connect/communities/{}".format(
                    task_options_with_id["communityid"]
                ),
                "urlPathPrefix": "test",
            },
        )

        with self.assertRaises(SalesforceException):
            cc_task._run_task()
