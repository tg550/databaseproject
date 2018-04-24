#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 03:28:49 2018

@author: denny
"""

from rect_3d import *
from rtree_3d import *
import unittest


class Pyrtree_Tester(unittest.TestCase):
    """setup class for unit tests."""
    def setUp(self):
        k = 5
        w = 20
        objects = {}
        id = 0
        for i in range(k):
            mn_y = i * w
            mx_y = mn_y + w
            for j in range(k):
                mn_x = j * w
                mx_x = mn_x + w
                for l in range(k):
                    mn_z = l * w
                    mx_z = mn_z + w                    
                    objects[id] = Rect(mn_x, mn_y, mn_z, mx_x, mx_y, mx_z)
                    id += 1
        self.objects = objects

    def test_rtree(self):
        t = RTree()
        for object in self.objects:
            t.insert(object, self.objects[object])
        self.assertEqual(len(self.objects), 1000)

        qr = Rect(5, 5, 5, 25, 25, 25)

        # find objects with mbrs intersecting with qr
        res = [r.leaf_obj() for r in t.query_rect(qr) if r.is_leaf()]
        print(len(rest))
        self.assertEqual(len(res), 4)
        res.sort()
        self.assertEqual(res, [0, 1, 10, 11])

        # vertices are shared by all coincident rectangles
        res = [r.leaf_obj(
        ) for r in t.query_point((20.0, 20.0)) if r.is_leaf()]
        self.assertEqual(len(res), 4)

        res = [r.leaf_obj() for r in t.query_point((21, 20)) if r.is_leaf()]
        self.assertEqual(len(res), 2)

        # single internal point
        res = [r.leaf_obj() for r in t.query_point((21, 21)) if r.is_leaf()]
        self.assertEqual(len(res), 1)

        # single external point
        res = [r.leaf_obj() for r in t.query_point((-12, 21)) if r.is_leaf()]
        self.assertEqual(len(res), 0)

        qr = Rect(5, 6, 65, 7)

        res = [r.leaf_obj() for r in t.query_rect((qr)) if r.is_leaf()]
        self.assertEqual(len(res), 4)


suite = unittest.TestSuite()
test_classes = [Pyrtree_Tester]
for i in test_classes:
    a = unittest.TestLoader().loadTestsFromTestCase(i)
    suite.addTest(a)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite)