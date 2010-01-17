# -*- coding: utf-8 -*-

try:
    from lxml import etree 
except ImportError:
    try:
        from lxml import cElementTree as etree
    except ImportError:
        try:
            import cElementTree as etree
        except ImportError:
            try:
                import elementtree.ElementTree
            except ImportError:
                raise ImportError('etree is needed')

from time import clock

def xml_to_dict(xml):
    root = etree.fromstring(xml)
    def parse(children):
        dic = {}
        for child in children:
            tag = child.tag
            if not child.getchildren():
                text = child.text
                dic[tag] = text
            else:
                dic[tag] = parse(iter(child.getchildren()))
        return dic
    return root.tag, parse(iter(root.getchildren()))

def dict_to_xml(base, root, dic):
    def make(itr):
        xml_part = ''
        for key, value in itr:
            if isinstance(value, dict):
                xml_part += '<%s>%s</%s>' % (key,  make(iter(value.iteritems())), key)
            elif value is None:
                xml_part += '<%s/>' % (key)
            else:
                xml_part += '<%s>%s</%s>' % (key,  value,  key)
        return xml_part
    return '%s<%s>%s</%s>' % (base, root, make(iter(dic.iteritems())), root)


if __name__ == '__main__':
    x = '''<?xml version="1.0"?>
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
    </InventoryFolderBase>'''
    
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
