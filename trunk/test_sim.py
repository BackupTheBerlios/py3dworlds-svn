import xmlrpclib

s = xmlrpclib.ServerProxy('http://cuonsim1.de:9300')
print s.expect_user({'last_name':'Tairov'})
