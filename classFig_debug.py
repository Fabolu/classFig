#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classFig import classFig

fig = classFig('PPT',(2,1),sharex=True,hspace=0.1,figshow=False)
fig.plot([1,2,3,2,1])
#fig.show()
fig.save('classFig_debug.png')
