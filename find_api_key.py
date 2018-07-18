##############################################################################
# Halo API Find owner group for API key
# Author: Sean Nicholson
# Version 1.0.0
# Date 07.17.2018
# v 1.0.0 - initial release
##############################################################################


import cloudpassage, yaml



def create_api_session(session):
    config_file_loc = "cloudpassage.yml"
    config_info = cloudpassage.ApiKeyManager(config_file=config_file_loc)
    session = cloudpassage.HaloSession(config_info.key_id, config_info.secret_key)
    return session


def find_api_key_owner(session):
    with open('cloudpassage.yml') as config_settings:
        script_options_info = yaml.load(config_settings)
        look_for_me = script_options_info['defaults']['search_api_key']
    api_results_list = cloudpassage.HttpHelper(session)
    list_of_groups = api_results_list.get_paginated("/v1/groups?per_page=1000", "groups", 20)
    for group in list_of_groups:
        query_url = "/v2/groups/" + group['id'] + "/api_keys"
        list_of_keys = api_results_list.get_paginated(query_url, "api_keys", 10)
        for key in list_of_keys:
            if key['key'] == look_for_me:
                print "Owner group is name = {0}, groupID = {1} \n group_path = {2}".format(group['name'], group['id'], group['group_path'])
                break

if __name__ == "__main__":
    api_session = None
    api_session = create_api_session(api_session)
    find_api_key_owner(api_session)
