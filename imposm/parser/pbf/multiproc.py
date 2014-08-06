# Copyright 2011 Omniscale GmbH & Co. KG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import multiprocessing
import threading

from imposm.parser.pbf.parser import PBFFile, PBFParser


class PBFParserProcess(PBFParser, threading.Thread):
    def __init__(self, pos_queue, *args, **kw):
        threading.Thread.__init__(self)
        PBFParser.__init__(self, *args, **kw)
        self.pos_queue = pos_queue

    def run(self):
        while True:
            pos = self.pos_queue.get()
            if pos is None:
                self.pos_queue.task_done()
                break
            self.parse(pos['filename'], offset=pos['blob_pos'],
                       size=pos['blob_size'])
            self.pos_queue.task_done()


class PBFMultiProcParser(object):
    nodes_tag_filter = None
    ways_tag_filter = None
    relations_tag_filter = None

    def __init__(self, pool_size, nodes_callback=None, ways_callback=None,
                 relations_callback=None, coords_callback=None, marshal_elem_data=False):
        self.pool_size = pool_size
        self.marshal = marshal_elem_data
        self.coords_callback = coords_callback
        self.nodes_callback = nodes_callback
        self.ways_callback = ways_callback
        self.relations_callback = relations_callback

    def parse(self, filename):
        pos_queue = multiprocessing.JoinableQueue(32)
        pool = []
        for _ in xrange(self.pool_size):
            thread = PBFParserProcess(pos_queue, nodes_callback=self.nodes_callback,
                                    coords_callback=self.coords_callback, ways_callback=self.ways_callback,
                                    relations_callback=self.relations_callback,
                                    nodes_tag_filter=self.nodes_tag_filter,
                                    ways_tag_filter=self.ways_tag_filter,
                                    relations_tag_filter=self.relations_tag_filter,
                                    marshal=self.marshal
            )
            pool.append(thread)
            thread.start()

        reader = PBFFile(filename)

        for pos in reader.blob_offsets():
            pos_queue.put(pos)

        pos_queue.join()

        for thread in pool:
            pos_queue.put(None)
        for thread in pool:
            thread.join()
