import requests
import json
import base64
import os
import yaml

class Github:
    def __init__(self):
        local_path = os.getcwd()
        config_file = local_path + '/testbed_config.yaml'
        with open(config_file, 'r') as stream:
            try:
                tb_data = yaml.load(stream)
                if 'git_testbed' in tb_data:
                    self.host_url = tb_data['git_testbed']['host_url']
                    self.headers = tb_data['git_testbed']['headers']

                    # Credentials for the GitHub Account
                    self.client_id = tb_data['git_testbed']['client_id']
                    self.client_secret = tb_data['git_testbed']['client_secret']

                    # OAuth endpoints given in the GitHub API documentation
                    self.authorization_base_url = tb_data['git_testbed']['authorization_base_url']
                    self.token_url = tb_data['git_testbed']['token_url']
                print(yaml.load(stream))
            except yaml.YAMLError as exc:
                print(exc)

    def get_tree(self,userName,repoName,sha):
        '''
        :param userName: UserName of owner of GitHub Repository
        :param repoName: Name of GitHub Repository
        :param sha: sha for the repository
        :return:
        '''
        self.userName = userName
        self.repoName = repoName
        self.sha = sha
        try:
            request_str = "{}/repos/{}/{}/git/trees/{}".format(self.host_url,self.userName, self.repoName,self.sha)
            print("Sending request Get tree api request : {}\n".format(request_str))
            response = requests.get(request_str, headers=self.headers)
            print("Get tree API response code : {}\n".format(response.status_code))
            json_data = response.json()
            print("Get tree API response : {}\n".format(json_data))
            #print(list(json_data.keys()))
            if response.status_code == 200:
                assert ['sha', 'url', 'tree', 'truncated'] == list(json_data.keys())
                if 'tree' in json_data:
                    tree = json_data['tree']
                    print("Found tree with paths: ")
                    for _path in tree:
                        print(_path["path"])
                return response.status_code
            elif response.status_code == 400:
                print("Unable to get tree for repo {} \nMessage : {} \n".format(self.repoName,json_data ["message"]))
                return response.status_code
            elif response.status_code == 404:
                print("Unable to get tree for repo {} \nMessage : {} \nInvalid userName or repoName or sha ".format(self.repoName,json_data ["message"]))
                return response.status_code
        except Exception as e:
            print(e)

    def get_contents_of_file(self,userName,repoName,fileName):
        '''

        :param userName: UserName of owner of GitHub Repository
        :param repoName: Name of GitHub Repository
        :param fileName: Name of file to fetch contents
        :return:
        '''
        self.userName = userName
        self.repoName = repoName
        self.fileName = fileName
        try:
            request_str = "{}/repos/{}/{}/contents/{}".format(self.host_url, self.userName, self.repoName, self.fileName)
            print("Sending request Get tree api request : {}\n".format(request_str))
            response = requests.get(request_str, headers=self.headers)
            print("Get tree API response code : {}\n".format(response.status_code))
            json_data = response.json()
            print("Get tree API response : {}\n".format(json_data))
            if response.status_code == 200:
                assert json_data["name"] == self.fileName and (json_data["type"] == "file" or "dir")
                return response.status_code
            elif response.status_code == 404:
                print("Unable to get contents of file or directory {} \nMessage : {} \nInvalid userName or repoName or fileName ".format(self.fileName, json_data["message"]))
                return response.status_code
        except Exception as e:
            print(e)

    def create_file(self,userName,repoName,contentPath,json_payload):
        '''
        :param userName: UserName of owner of GitHub Repository
        :param repoName: Name of GitHub Repository
        :param contentPath: Name /path for new file
        :return:
        '''
        self.userName = userName
        self.repoName = repoName
        self.contentPath = contentPath
        self.json_payload = json_payload
        content_str = json_payload["committer"]["content"]
        content_str = content_str.encode("utf-8")
        content_str = base64.b64encode(content_str)
        json_payload["committer"]["content"] = content_str.decode("utf-8")
        print(content_str)
        try:
            request_str = "{}/repos/{}/{}/contents/{}".format(self.host_url, self.userName, self.repoName, self.contentPath)
            print("Sending request Put / Create file api request : {}\n".format(request_str))
            response = requests.put(request_str, data = json.dumps(self.json_payload), auth = (self.client_id, self.client_secret))
            print("Get tree API response code : {}\n".format(response.status_code))
            json_data = response.json()
            print("Get tree API response : {}\n".format(json_data))
            if response.status_code == 201:
                assert json_data["content"]["path"] == self.contentPath
                return response.status_code
            elif response.status_code == 422:
                print("Unable to create file or directory {} \nMessage : {} \n".format(self.contentPath, json_data["message"]))
                return response.status_code
            elif response.status_code == 404:
                print("Unable to create file or directory {} \nMessage : {} \nInvalid userName or repoName or fileName ".format(self.contentPath, json_data["message"]))
                return response.status_code
        except Exception as e:
            print(e)

    def list_branches(self,userName,repoName):
        '''
        :param userName: UserName of owner of GitHub Repository
        :param repoName: Name of GitHub Repository
        :return:
        '''
        self.userName = userName
        self.repoName = repoName
        try:
            request_str = "{}/repos/{}/{}/branches".format(self.host_url, self.userName, self.repoName)
            print("Sending request get list branch api request : {}\n".format(request_str))
            response = requests.get(request_str, headers=self.headers)
            print("Get tree API response code : {}\n".format(response.status_code))
            json_data = response.json()
            print("Get tree API response : {}\n".format(json_data))
            if response.status_code == 200:
                json_data = json_data[0]
                print(list(json_data.keys()))
                assert ['name', 'commit'] == list(json_data.keys())
                return response.status_code
            elif response.status_code == 404:
                print("Unable to list repo branches: {} \nMessage : {} \nInvalid userName or repoName".format(self.repoName, json_data["message"]))
                return response.status_code
        except Exception as e:
            print(e)

    def change_repo_des(self,userName,repoName,json_payload):
        '''
        :param userName: UserName of owner of GitHub Repository
        :param repoName: Name of GitHub Repository
        :param json_payload: payload to be sent with request
        :return:
        '''
        self.userName = userName
        self.repoName = repoName
        self.json_payload = json_payload
        try:
            request_str = "{}/repos/{}/{}".format(self.host_url, self.userName, self.repoName)
            print("Sending request PATCH change repo description api request : {}\n".format(request_str))
            response = requests.patch(request_str, data = json.dumps(self.json_payload),  auth = (self.client_id,self.client_secret))
            print("Change Repo Description API response code : {}\n".format(response.status_code))
            json_data = response.json()
            print("Change Repo Description API response : {}\n".format(json_data))
            if response.status_code == 200:
                return response.status_code
            elif response.status_code == 400:
                print("Unable to change repo description \nMessage : {} \nInvalid userName or repoName".format(json_data["message"]))
                return response.status_code
        except Exception as e:
            print(e)
        pass

    def create_issue(self,userName,repoName,json_payload):
        '''
        :param userName: UserName of owner of GitHub Repository
        :param repoName: Name of GitHub Repository
        :param json_payload: payload to be sent with request
        '''
        self.userName = userName
        self.repoName = repoName
        self.json_payload = json_payload
        try:

            json_payload = {
                "title": "Testing the create issue API"
            }
            request_str = "{}/repos/{}/{}/issues".format(self.host_url, self.userName, self.repoName)
            print("Sending POST create issue api request : {}\n".format(request_str))
            response = requests.post(request_str, data= json.dumps(self.json_payload),auth = (self.client_id,self.client_secret) )
            print("Create issue API response code : {}\n".format(response.status_code))
            json_data = response.json()
            print("Change Repo Description API response : {}\n".format(json_data))
            if response.status_code == 201:
                return response.status_code
            elif response.status_code == 422:
                print("Failed to create issue {} \nMessage : {} \n".format(json_payload, json_data["message"]))
                return response.status_code
            elif response.status_code == 404:
                print("Failed to list repo branches: {} \nMessage : {} \n".format(json_payload, json_data["message"]))
                return response.status_code
        except Exception as e:
            print(e)
        pass


    def create_pull_request(self,userName,repoName,json_payload):
        '''
        :param userName: UserName of owner of GitHub Repository
        :param repoName: Name of GitHub Repository
        :param json_payload: payload to be sent with request
        :return:
        '''
        self.userName = userName
        self.repoName = repoName
        self.json_payload = json_payload
        print(self.client_secret)
        try:
            request_str = "{}/repos/{}/{}/pulls".format(self.host_url, self.userName, self.repoName)

            print("Sending POST create pull request api request : {}\n".format(request_str))
            print(self.json_payload)
            response = requests.post(request_str, data=json.dumps(self.json_payload), auth=(self.client_id,self.client_secret))
            print("Create pull request API response code : {}\n".format(response.status_code))
            json_data = response.json()
            print("Create pull request API response : {}\n".format(json_data))
            if response.status_code == 200:
                return response.status_code
            elif response.status_code == 401:
                print("Unable to pull request for {} \nMessage : {} \n".format(self.repoName, json_data["message"]))
                return response.status_code
            elif response.status_code == 422:
                print("Unable to pull request for {} \nMessage : {} \n".format(self.repoName, json_data["message"]))
                return response.status_code
            elif response.status_code == 404:
                print("Unable to pull request for {} \nMessage : {} \nInvalid userName or repoName".format(self.repoName, json_data["message"]))
                return response.status_code
        except Exception as e:
            print(e)
        pass

if __name__ == '__main__':
    Github()

