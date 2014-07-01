"""
    Functionality Provided:
    Group:
        + retrieve - IsRegisteredOrAnyInstructor
        + update, delete - IsOwner
        - concepts - IsRegisteredOrAnyInstructor
        - reorder_concepts - IsOwner
        - add_concept - IsOwner
"""
from django.shortcuts import get_object_or_404

from courseware.models import Group, Concept
from courseware.serializers import GroupSerializer, ConceptSerializer
from courseware import playlist
from courseware.permissions import IsOwnerOrReadOnly, IsOwner

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import link, action

from document.models import Document


class GroupViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def destroy(self, request, pk=None, *args):
        group = get_object_or_404(Group, pk=pk)
        _course = group.course
        _course.playlist = playlist.delete(_course.playlist, pk=pk)
        _course.save()
        return super(GroupViewSet, self).destroy(request, pk)

    @link(permission_classes=((IsOwner, )))
    def concepts(self, request, pk=None):
        """
            Function to get all the concepts in a course
        """
        group = get_object_or_404(Group, pk=pk)
        self.check_object_permissions(request=request, obj=group.course)
        concepts = Concept.objects.filter(group=group)
        serializer = ConceptSerializer(concepts, many=True)
        if len(serializer.data) == 0:
            return Response([])
        _playlist = playlist.to_array(group.playlist)
        N = len(_playlist)
        ordered_data = [""]*N
        for i in range(N):
            ordered_data[i] = serializer.data[_playlist[i][1]]
        return Response(ordered_data)

    @link(permission_classes=((IsOwnerOrReadOnly, )))
    def published_concepts(self, request, pk=None):
        """
            Function to get all the concepts in a course
        """
        group = get_object_or_404(Group, pk=pk)
        self.check_object_permissions(request=request, obj=group.course)
        concepts = Concept.objects.filter(group=group)
        _playlist = playlist.to_array(group.playlist)
        N = len(_playlist)
        ordered_data = []
        for i in range(N):
            concept = concepts[_playlist[i][1]]
            if concept.is_published:
                #  TODO: check if append does not take O(n) time
                ordered_data.append(concept)
        serializer = ConceptSerializer(ordered_data, many=True)
        return Response(serializer.data)

    @action(
        methods=['PATCH'],
        permission_classes=((IsOwnerOrReadOnly, )),
        serializer_class=GroupSerializer)
    def reorder_concepts(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        self.check_object_permissions(request=request, obj=group.course)
        myplaylist = request.DATA['playlist']
        newplaylist = playlist.is_valid(myplaylist, group.playlist)
        if newplaylist is not False:
            group.playlist = newplaylist
            group.save()
            return Response(group.playlist)
        else:
            content = "Given order data does not have the correct format"
            return Response(content, status.HTTP_404_NOT_FOUND)

    @action(
        methods=['POST'],
        permission_classes=((IsOwnerOrReadOnly, )),
        serializer_class=ConceptSerializer
        )
    def add_concept(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        self.check_object_permissions(request, group.course)
        serializer = ConceptSerializer(data=request.DATA)
        if serializer.is_valid():
            document = Document(
                title='dummy',
                description='dummy'
                )
            document.save()
            concept = Concept(
                group=group,
                title_document=document,
                title=serializer.data['title'],
                description=serializer.data['description']
                )
            if request.FILES != {}:
                concept.image = request.FILES['image']
            concept.save()
            group.playlist = playlist.append(concept.id, group.playlist)
            group.save()
            return Response(ConceptSerializer(concept).data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)
