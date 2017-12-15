# GitHub_API_Testing
Testsuite for testing some GitHub API's

**************************
Contents of the Test suite
**************************

    Testbed Configuration :
    ======================

    testbed_config.yaml   -   Provides login credentials, headers and authentication details for connecting to GitHub

    API Library Module :
    ===================

    api_lib.py   - Provides methods to call the different GitHub API's

    Test Data :
    ==========

    Tests are run using test data extracted from the following file.
    Maintained separate input files for each api, Easy to maintain and add more test data

    test_data_change_repo_des.json
    test_data_create_file.json
    test_data_create_issue.json
    test_data_get_contents.json
    test_data_get_tree.json
    test_data_list_branches.json
    test_data_pull_request.json

    Test scripts :
    ============

    test_git_apis.py  -  Contains tests for api's given below:

    ### Git Data Operations

    * List the tree contents
    * Return the contents of a file
    * Create a file

    ### Repo Operations

    * List the branches
    * Change the repo description
    * Add a new issue
    * Create a pull request


***********************
Test suite Dependencies
***********************

    Following is a list of major dependencies

    requests           http://docs.python-requests.org/en/master/
    requests-oauthlib
    pyyaml             https://pypi.python.org/pypi/PyYAML
    ddt                https://pypi.python.org/pypi/ddt, https://ddt.readthedocs.io/en/latest/example.html

    Python version : Python 3.6

********************
Testsuite Execution
********************

    Test executed by creating virtual environment

    1.) Command for creating virtual env

        python3 -m venv {environment name}

    2.) Command for running

        nosetests -v -s test_git_apis.py
