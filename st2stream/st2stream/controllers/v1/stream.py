# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import six

from st2common import log as logging
from st2common.router import Response
from st2common.util.jsonify import json_encode
from st2stream.listener import get_listener

LOG = logging.getLogger(__name__)


def format(gen):
    message = '''event: %s\ndata: %s\n\n'''

    for pack in gen:
        if not pack:
            # Note: gunicorn wsgi handler expect bytes, not unicode
            yield six.binary_type('\n')
        else:
            (event, body) = pack
            # Note: gunicorn wsgi handler expect bytes, not unicode
            yield six.binary_type(message % (event, json_encode(body, indent=None)))


class StreamController(object):
    def get_all(self):
        def make_response():
            res = Response(content_type='text/event-stream',
                           app_iter=format(get_listener().generator()))
            return res

        stream = make_response()

        return stream


stream_controller = StreamController()
