# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 19:18:46 2016

@author: joerod
"""
import dropbox
import json

client = dropbox.client.DropboxClient('')
#print 'linked account: ', client.account_info()

folder_metadata = client.metadata('/')

#Prints out pretty json result
#print json.dumps(folder_metadata, indent=4)

#finds specific value
#print json.dumps(folder_metadata['contents'][0]['path'], indent=4) 

for i in folder_metadata['contents']:
    print i['path'],i['size']
