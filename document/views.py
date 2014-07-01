from django.shortcuts import get_object_or_404

from document.models import Document, Section
from document.serializers import DocumentSerializer, SectionSerializer, AddSectionSerializer
from courseware import playlist
from courseware.models import Course

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action



# Create your views here.


class DocumentViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    model = Document
    serializer_class = DocumentSerializer

    def retrieve(self, request, pk=None, *args):
        d = get_object_or_404(Document, pk=pk)
        obj = d.to_dict()
        return Response(obj)

    def destroy(self, request, pk=None, *args):
        document = get_object_or_404(Document, pk=pk)
        _course = Course.objects.filter(pages__pk=pk)
        if len(_course) > 0:
            _course = _course[0]
            _course.page_playlist = playlist.delete(_course.page_playlist,
                                                    pk=pk)
            _course.save()
        return super(DocumentViewSet, self).destroy(request, pk, *args)

    @action(methods=['PATCH'], serializer_class=DocumentSerializer)
    def reorder_sections(self, request, pk=None):
        document = get_object_or_404(Document, pk=pk)
        #self.check_object_permissions(request, _course)
        myplaylist = request.DATA['playlist']
        newplaylist = playlist.is_valid(myplaylist, document.playlist)
        if newplaylist is not False:
            document.playlist = newplaylist
            document.save()
            return Response(document.to_dict())
        else:
            content = "Given order data does not have the correct format"
            return Response(content, status.HTTP_404_NOT_FOUND)

    @action(methods=['POST'], serializer_class=AddSectionSerializer)
    def add_section(self, request, pk=None):
        document = get_object_or_404(Document, pk=pk)
        serializer = AddSectionSerializer(data=request.DATA)
        if serializer.is_valid():
            if request.FILES and request.FILES['file']:
                section = Section(
                    document=document,
                    title=serializer.data['title'],
                    description=serializer.data['description'],
                    file=request.FILES['file'])
            else:
                section = Section(
                    document=document,
                    title=serializer.data['title'],
                    description=serializer.data['description'])
            section.save()
            document.playlist = playlist.append(section.id, document.playlist)
            document.save()
            return Response(SectionSerializer(section).data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)


class SectionViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """ViewSet for section class"""
    model = Section
    serializer_class = SectionSerializer
    def partial_update(self, request, pk=None, *args):
        if 'file' in request.DATA:
            request.DATA.pop('file', None)
        return super(SectionViewSet, self).partial_update(request, pk, *args)

    def destroy(self, request, pk=None, *args):
        section = get_object_or_404(Section, pk=pk)
        document = section.document
        document.playlist = playlist.delete(document.playlist, pk=pk)
        document.save()
        return super(SectionViewSet, self).destroy(request, pk, *args)
