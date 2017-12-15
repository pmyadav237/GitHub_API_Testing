import os
from api_lib import Github
from ddt import ddt, unpack, file_data
api_handle = Github()

local_path = os.getcwd()
test_files = [local_path + td for td in ['/test_data_get_tree.json','/test_data_get_contents.json', '/test_data_create_file.json',
                                        '/test_data_list_branches.json', '/test_data_change_repo_des.json',
                                       '/test_data_create_issue.json', '/test_data_pull_request.json' ]]

@ddt
class Test_GitHub_API():

    @file_data(test_files[0])
    @unpack
    def test_get_tree(self, values):
        result = api_handle.get_tree(values[0], values[1], values[2])
        assert result == values[3]

    @file_data(test_files[1])
    @unpack
    def test_get_contents_of_file(self, values):
        result = api_handle.get_contents_of_file(values[0], values[1], values[2])
        assert result == values[3]

    @file_data(test_files[2])
    @unpack
    def test_create_file(self,values):
        result = api_handle.create_file(values[0], values[1], values[2])
        assert result == values[3]

    @file_data(test_files[3])
    @unpack
    def test_list_branches(self, values):
        result = api_handle.list_branches(values[0], values[1])
        assert result == values[2]


    @file_data(test_files[4])
    @unpack
    def test_change_repo_des(self, values):
        result = api_handle.change_repo_des(values[0], values[1], values[2])
        assert result == values[3]

    @file_data(test_files[5])
    @unpack
    def test_create_issue(self,values):
        result = api_handle.create_issue(values[0],values[1],values[2])
        assert result == values[3]

    @file_data(test_files[6])
    @unpack
    def test_create_pull_request(self, values):
        result = api_handle.create_pull_request(values[0], values[1],values[2])
        assert result == values[3]

