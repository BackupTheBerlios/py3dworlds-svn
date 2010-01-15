# -*- coding: utf-8 -*-

try:
    from lxml import etree
except ImportError:
    from lxml import cElementTree as etree

def parse_to_dict(xml):
    root = etree.fromstring(xml)
    dic = {}
    for child in root.getchildren():
        tag = child.tag
        text = child.text
        dic[tag] = text
    return dic
    
def parse_to_xml(root,  dic):
    xml = '<' + root + '>'
    for key,  value in dic.iteritems():
        xml += '<%s>%s</%s>' % (key,  value,  key)
    xml += '</' + root + '>'
