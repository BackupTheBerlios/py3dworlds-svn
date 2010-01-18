#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This module produces bad XML, don't use this
## except you know what you are doing

from dicxml import xml_to_dict, dict_to_xml
from re import split as re_split, match as re_match

def more_roots_to_dict(xml):
    xml = xml.strip()
    if re_match('<[\s]*\?[\w, \', ", \., \,, =, -]+\?[\s]*>', xml):
        xml = re_split('\?[\s]*>', xml, 1)[1]
    ret = xml_to_dict(''.join(['<randomroot>', xml, '</randomroot>']))[1]
    return ret.keys()[0], ret.values()[0]

def more_roots_to_xml(base, root, *args):
    return ''.join([base] + [dict_to_xml('', root, i) for i in args if not i is None])

if __name__ == '__main__':
    b_xml = '''
    < ? version=\'1.0\' standalone = "1\' ?\t     >
    <x/>
    <x><foo>asd</foo><bar/></x>
    <x><foo1>ass</foo1></x>
    <x/>''' # wtf! root is None
    
    m_roots = [{'foo' : 'test', 'bar' : None}]*3
    
    mrtd = more_roots_to_dict(b_xml)
    print mrtd
    print more_roots_to_xml('<? version="1"?>', mrtd[0], *mrtd[1])