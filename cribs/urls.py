'''
Created on Jun 17, 2013
@author: aryaveer
'''

from django.conf.urls import patterns, url

urlpatterns = patterns('cribs.views',
    url(r'^create/(?P<assignmentID>\d+)$', 'createCrib', name='cribs_createcrib'),
    url(r'^crib/(?P<assignmentID>\d+)$', 'myCribs', name='cribs_mycribs'),
    url(r'^cribdetails/(?P<cribID>\d+)$', 'cribDetail', name='cribs_cribDetail'),
    url(r'^allcribs/(?P<assignmentID>\d+)$', 'allCribs', name='cribs_allcribs'),
    url(r'^edit/(?P<cribID>\d+)$', 'editCrib', name='cribs_editcrib'),
    url(r'^close/(?P<cribID>\d+)$', 'closeCrib', name='cribs_closecrib'),
    url(r'^open/(?P<cribID>\d+)$', 'reopenCrib', name='cribs_reopencrib'),
    url(r'^comments/add/(?P<cribID>\d+)$', 'postComment', name='cribs_postcomment'),
    url(r'^comments/edit/(?P<commentID>\d+)$', 'editComment', name='cribs_editcomment'),
)