#!/usr/bin/env python
# -*- coding: utf-8 -*-

for mod in ['lxml.etree', 'lxml.cElementTree', 'cElementTree',
            'elementtree.ElementTree', 'xml.etree.cElementTree']:
    try:
        globals()['etree'] = __import__(mod, fromlist=[mod.split('.')[-1]])  
    except ImportError:
        pass
    else:
        break
if not 'etree' in globals():
    raise ImportError('etree is needed')

def xml_to_dict(xml):
    root = etree.fromstring(xml.strip())
    def parse(children):
        dic = {}
        for child in children:
            tag = child.tag
            if not child.getchildren():
                text = child.text
                if not tag in dic:
                    dic[tag] = text
                elif isinstance(dic[tag], list):
                    dic[tag].append(text)
                else:
                    dic[tag] = [dic[tag], text]
            else:
                p = parse(iter(child.getchildren()))
                if not tag in dic:
                    dic[tag] = p
                elif isinstance(dic[tag], list):
                    dic[tag].append(p)
                else:
                    dic[tag] = [dic[tag], p]
        return dic
    return root.tag, parse(iter(root.getchildren()))

## Slow!!!
#def dict_to_xml(base, root, dic):
#    def make(itr):
#        xml_part = ''
#        for key, value in itr:
#            if isinstance(value, dict):
#                xml_part += '<%s>%s</%s>' % (key,  make(iter(value.iteritems())), key)
#            elif isinstance(value, list):
#                for i in value:
#                    xml_part += make(iter(i.iteritems()))
#            elif value is None:
#                xml_part += '<%s/>' % (key)
#            else:
#                xml_part += '<%s>%s</%s>' % (key,  value,  key)
#        return xml_part
#    return '%s<%s>%s</%s>' % (base, root, make(iter(dic.iteritems())), root)

## Fast!!!
def dict_to_xml(base, root, dic):
    root = etree.Element(root)
    def add(parent, itr):
        for key, value in itr:
            if isinstance(value, dict):
                add(etree.SubElement(parent, key), iter(value.iteritems()))
            elif isinstance(value, list):
                for i in value:
                    if isinstance(i, dict):
                        add(etree.SubElement(parent, key), iter(i.iteritems()))
                    else:
                        etree.SubElement(parent, key).text = i
            elif value is None:
                etree.SubElement(parent, key)
            else:
                etree.SubElement(parent, key).text = value
        return parent
    return ''.join([base, etree.tostring(add(root, iter(dic.iteritems())))])

if __name__ == '__main__':
    from time import clock, sleep
    x = '''<?xml version="1.0"?>
    <root>
        <InventoryFolderBase>
            <Name>My Inventory</Name>
            <ID>
                <Guid>3e1a8134-f9d7-40a1-9a01-7fff99ac8536</Guid>
            </ID>
            <Owner>
                <test>TEST!</test>
                <Guid>fb65174f-2dde-4c1e-ba13-1a776d6864fd</Guid>
            </Owner>
            <ParentID>
                <Guid>00000000-0000-0000-0000-000000000000</Guid>
            </ParentID>
            <Type>8</Type>
            <Version>1</Version>
            <Version>2</Version>
            <selfClosing/>
        </InventoryFolderBase>
    </root>'''
    
    start2dict = clock()
    td = xml_to_dict(x)
    end2dict = clock()
    print td
    start2xml = clock()
    tx = dict_to_xml('<?xml version="1.0"?>', *td)
    end2xml = clock()
    print tx
    #print '\n'.join([i.strip() for i in x.splitlines()])
    print 'Zeit für xml_to_dict', end2dict - start2dict, 'Sekunden'
    print 'Zeit für dict_to_xml', end2xml - start2xml, 'Sekunden'
    print len(x.splitlines()), 'Zeilen'
    '''
    
    from threading import Thread
    
    def test_threading():
        td = xml_to_dict(x)
        tx = dict_to_xml('<?xml version="1.0"?>', *td)
        print 'Zeit:', clock() - start,
        print 'Done \n' 
    
    threads = [Thread(target=test_threading) for i in range(50)]
    
    start = clock()
    for ii in threads:
        ii.start()
        print ii, 'started'
        #sleep(0.1)
    ii.join()
    print len(x.splitlines()), 'Zeilen'
    '''
