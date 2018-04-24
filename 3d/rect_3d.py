#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 00:41:48 2018

@author: denny
"""

import math

class Rect(object):
    
    __slots__ = ("x","y","z","xx","yy","zz", "swapped_x", "swapped_y","swapped_z") # bot-left, top-right

    def __init__(self, minx,miny,minz,maxx,maxy,maxz):
    # initialize, check points to be bl,tr
        self.swapped_x = (maxx < minx)
        self.swapped_y = (maxy < miny)
        self.swapped_z = (maxz < minz)
        self.x = minx
        self.y = miny
        self.z = minz
        self.xx = maxx
        self.yy = maxy
        self.zz = maxz

        if self.swapped_x: self.x,self.xx = maxx,minx
        if self.swapped_y: self.y,self.yy = maxy,miny
        if self.swapped_z: self.z,self.zz = maxz,minz

    def coords(self):
        # return coordinates of points
        return self.x,self.y,self.z,self.xx,self.yy,self.zz

    def overlap(self, orect):
        # return overlap area
        return self.intersect(orect).area()

    def write_raw_coords(self, toarray, idx):
        # turn coords to array
        toarray[idx] = self.x
        toarray[idx+1] = self.y
        toarray[idx+2] = self.z
        toarray[idx+3] = self.xx
        toarray[idx+4] = self.yy
        toarray[idx+5] = self.zz
        if (self.swapped_x):
            toarray[idx] = self.xx
            toarray[idx+3] = self.x
        if (self.swapped_y):
            toarray[idx + 1] = self.yy
            toarray[idx + 4] = self.y
        if (self.swapped_y):
            toarray[idx + 2] = self.zz
            toarray[idx + 5] = self.z       


    def area(self):
        # return area of rect
        w = self.xx - self.x
        h = self.yy - self.y
        l = self.zz - self.z
        return w * h * l

    def extent(self):
        # return bl coord and w,h
        x = self.x
        y = self.y
        z = self.z
        return (x,y,z,self.xx-x,self.yy-y,self.zz-z)

    def grow(self, amt):
        # increase size of rect
        a = amt * 0.5
        return Rect(self.x-a,self.y-a,self.z-a,self.xx+a,self.yy+a,self.zz+a)

    def intersect(self,o):
        # return intersect coord of rects 
        if self is NullRect: return NullRect
        if o is NullRect: return NullRect

        nx,ny,nz= max(self.x,o.x),max(self.y,o.y),max(self.z,o.z)
        nx2,ny2,nz2 = min(self.xx,o.xx),min(self.yy,o.yy),min(self.zz,o.zz)
        w,h,l = nx2-nx, ny2-ny, nz2-nz

        if w <= 0 or h <= 0 or l <= 0: return NullRect

        return Rect(nx,ny,nz,nx2,ny2,nz2)

    def does_containpoint(self,p):
        # check if point is inside a rect
        x,y,z = p
        return (x >= self.x and x <= self.xx and y >= self.y and y <= self.yy and z >= self.z and z <= self.zz)

    def does_contain(self,o):
        # check if rect is inside of another rect
        return self.does_containpoint( (o.x,o.y,o.z) ) and self.does_containpoint( (o.xx,o.yy,o.zz) )

    def does_intersect(self,o):
        # check if rects are intersect
        return (self.intersect(o).area() > 0)

    def union(self,o):
        # return rect of combining two rects
        if o is NullRect: return Rect(self.x,self.y,self.z,self.xx,self.yy,self.zz)
        if self is NullRect: return Rect(o.x,o.y,o.z,o.xx,o.yy,o.zz)
        
        x = self.x
        y = self.y
        z = self.z
        xx = self.xx
        yy = self.yy
        zz = self.zz
        ox = o.x
        oy = o.y
        oz = o.z
        oxx = o.xx
        oyy = o.yy
        ozz = o.zz

        nx = x if x < ox else ox
        ny = y if y < oy else oy
        nz = z if z < oz else oz
        nx2 = xx if xx > oxx else oxx
        ny2 = yy if yy > oyy else oyy
        nz2 = zz if zz > ozz else ozz

        res = Rect(nx,ny,nz,nx2,ny2,nz2)

        return res
        
#    def union_point(self,o):
#        x,y = o
#        return self.union(Rect(x,y,x,y))

    def diagonal_sq(self):
        # return rect diagonal's square
        if self is NullRect: return 0
        w = self.xx - self.x
        h = self.yy - self.y
        l = self.zz - self.z
        return w*w + h*h + l*l
    
    def diagonal(self):
        # return rect diagonal distance
        return math.sqrt(self.diagonal_sq())

NullRect = Rect(0.0,0.0,0.0,0.0,0.0,0.0)
NullRect.swapped_x = False
NullRect.swapped_y = False
NullRect.swapped_z = False

def union_all(kids):
    # return combining all rects
    cur = NullRect
    for k in kids: cur = cur.union(k.rect)
    assert(False ==  cur.swapped_x)
    return cur
