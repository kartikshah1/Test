'''
Created on Jun 17, 2013
@author: aryaveer
'''

from django import forms


class CribForm(forms.Form):
    title = forms.CharField(max_length=512)
    crib_detail = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="Add your comment")