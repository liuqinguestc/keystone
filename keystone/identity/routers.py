# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""WSGI Routers for the Identity service."""

from keystone.common import json_home
from keystone.common import router
from keystone.common import wsgi
from keystone.identity import controllers


class Routers(wsgi.RoutersBase):

    _path_prefixes = ('users', )

    def append_v3_routers(self, mapper, routers):
        user_controller = controllers.UserV3()
        routers.append(
            router.Router(user_controller,
                          'users', 'user',
                          resource_descriptions=self.v3_resources))

        self._add_resource(
            mapper, user_controller,
            path='/users/{user_id}/password',
            post_action='change_password',
            rel=json_home.build_v3_resource_relation('user_change_password'),
            path_vars={
                'user_id': json_home.Parameters.USER_ID,
            })

        group_controller = controllers.GroupV3()

        self._add_resource(
            mapper, group_controller,
            path='/users/{user_id}/groups',
            get_head_action='list_groups_for_user',
            rel=json_home.build_v3_resource_relation('user_groups'),
            path_vars={
                'user_id': json_home.Parameters.USER_ID,
            })
