'''
Created on Feb 27, 2014
@author: aryaveer
'''

from django.conf.urls import patterns, url

urlpatterns = patterns('download.views',
    url(r'^downloadall/(?P<assignmentID>\d+)$', 'download_all_zipped', name='download_download_all_zipped'),
    url(r'^assignment/data/(?P<assignmentID>\d+)$', 'download_assignment_files', name='download_downloadassignmentfiles'),
)