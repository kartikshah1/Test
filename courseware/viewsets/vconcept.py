"""
    Functionality provided:
    Concept:
        + retrieve: (IsRegisteredOrAnyInstructor)
        + update, delete: (IsOwner)

        - playlist - (IsRegisteredOrAnyInstructor)
        - reorder - (IsOwner)
        - add_video, add_element, add_quiz, add_document - (IsOwner)
        - add_existing_quiz, add_existing_document - (IsOwner)
        - delete_element - (IsOwner)
        - get_concept_page_data - (IsRegisteredOrAnyInstructor)
        - quizzes - (IsRegisteredOrAnyInstructor) (TODO)
"""

from django.shortcuts import get_object_or_404

from elearning_academy.settings import DEFAULT_CONCEPT_IMAGE

from courseware.models import Course, Group, Concept
from courseware.serializers import ConceptSerializer, AddQuizSerializer
from courseware import playlist, typed_playlist
from courseware.permissions import IsOwnerOrReadOnly, IsOwner

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import link, action

from concept.models import ConceptQuizHistory, ConceptDocumentHistory
from concept.serializers import ConceptDocumentHistorySerializer, \
    ConceptQuizHistorySerializer
from discussion_forum.models import DiscussionForum, Tag
from document.models import Document
from document.serializers import DocumentSerializer
from video.models import Video, VideoHistory
from video.serializers import VideoSerializer, AddVideoSerializer, VideoHistorySerializer
from quiz.serializers import QuizSerializer
from quiz.models import Quiz
from video.views import import_quiz_camtasia8

from elearning_academy.permissions import InInstructorOrContentDeveloperMode
import json


class ConceptViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    ViewSet for Concept class
    """
    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def destroy(self, request, pk=None):
        """
            Delete a Concept if owned by user and in playlist of its group
        """
        concept = get_object_or_404(Concept, pk=pk)
        group = concept.group
        new_playlist = playlist.delete(group.playlist, pk=pk)
        if not new_playlist:
            return Response({
                "detail": "Object not found in your Group"
                }, status.HTTP_404_NOT_FOUND)
        group.playlist = new_playlist
        group.save()
        return super(ConceptViewSet, self).destroy(request, pk)

    def playlist_as_array(self, request, pk=None, with_history=False):
        """
        Gets all the elements in the playlist
        """
        concept = get_object_or_404(Concept, pk=pk)
        #videos_obj = concept.videos.all()
        videos_obj = []
        for elem in json.loads(concept.playlist):
            if elem[2] == 0:
                videos_obj.append(Video.objects.get(pk=elem[0]))
        pages_obj = concept.pages.all()
        #pages_obj = []
        #for elem in json.loads(concept.playlist):
        #    if elem[2] == 2:
        #        pages_obj.append(Document.objects.get(pk=elem[0]))

        quizzes_obj = concept.quizzes.all()

        videos = VideoSerializer(videos_obj, many=True)
        pages = [page.to_dict() for page in pages_obj]
        quizzes = QuizSerializer(quizzes_obj, many=True)
        _playlist = typed_playlist.to_array(concept.playlist)

        if with_history:
            videos_history = []
            for video in videos_obj:
                videohistory = VideoHistory.objects.filter(video=video,
                                                           user=request.user)
                if (len(videohistory) == 0):
                    videohistory = VideoHistory(video=video, user=request.user)
                    videohistory.save()
                else:
                    videohistory = videohistory[0]
                videos_history.append(
                    VideoHistorySerializer(videohistory).data)

            quizzes_history = []
            for quiz in quizzes_obj:
                quizhistory = ConceptQuizHistory.objects.filter(
                    quiz=quiz,
                    user=request.user)
                if (len(quizhistory) == 0):
                    quizhistory = ConceptQuizHistory(
                        quiz=quiz,
                        user=request.user)
                    quizhistory.save()
                else:
                    quizhistory = quizhistory[0]
                quizzes_history.append(
                    ConceptQuizHistorySerializer(quizhistory).data)

            pages_history = []
            for document in pages_obj:
                documenthistory = ConceptDocumentHistory.objects.filter(
                    document=document,
                    user=request.user)
                if (len(documenthistory) == 0):
                    documenthistory = ConceptDocumentHistory(
                        document=document,
                        user=request.user)
                    documenthistory.save()
                else:
                    documenthistory = documenthistory[0]
                pages_history.append(
                    ConceptDocumentHistorySerializer(documenthistory).data)

        ordered_data = []
        for elem in _playlist:
            if elem[2] == 0:
                next_item = {
                    'type': 'video',
                    'content': videos.data[elem[1]]
                }
                if with_history:
                    next_item['history'] = videos_history[elem[1]]
            elif elem[2] == 1:
                next_item = {
                    'type': 'quiz',
                    'content': quizzes.data[elem[1]]
                }
                if with_history:
                    next_item['history'] = quizzes_history[elem[1]]
            elif elem[2] == 2:
                next_item = {
                    'type': 'document',
                    'content': pages[elem[1]]
                }
                if with_history:
                    next_item['history'] = pages_history[elem[1]]
            ordered_data.append(next_item)
        return ordered_data

    @action(methods=['POST'], permission_classes=((IsOwner, )))
    def publish(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        concept.is_published = not concept.is_published
        if concept.is_published:
            msg = "Published " + concept.title

            ## Create a tag by the same name as the concept name
            ## TODO: Better way to do this?
            ## TODO: What diff b/w tag_name and tag_title?
            ## TODO: Delete tag on un-publish
            group = get_object_or_404(Group, pk=concept.group_id)
            course_id = group.course_id
            forum = get_object_or_404(DiscussionForum,pk=course_id)
            tag = Tag(forum=forum)
            tag.tag_name = concept.title
            tag.title = concept.title
            tag.save()
        else:
            msg = "Un-Published " + concept.title
        concept.save()

        return Response({"msg": msg}, status.HTTP_200_OK)

    @link(permission_classes=((IsOwnerOrReadOnly, )))
    def playlist(self, request, pk=None):
        """ Return the playlist as a response"""
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        return Response(self.playlist_as_array(request, pk))

    @action(methods=['PATCH'], permission_classes=((IsOwnerOrReadOnly,)))
    def reorder(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        myplaylist = request.DATA['playlist']
        print myplaylist
        newplaylist = typed_playlist.is_valid(myplaylist, concept.playlist)
        if newplaylist is not False:
            concept.playlist = newplaylist
            concept.save()
            return Response(self.playlist_as_array(request, pk))
        else:
            content = "Given order data does not have the correct format"
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            permission_classes=((IsOwnerOrReadOnly, )),
            serializer_class=VideoSerializer)
    def add_video(self, request, pk=None):
        """
            Add video in the given concept
        """
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        serializer = AddVideoSerializer(data=request.DATA)
        if serializer.is_valid():
            if 'other_file' in request.FILES:
                video = Video(
                    title=serializer.data['title'],
                    content=serializer.data['content'],
                    video_file=request.FILES['video_file'],
                    other_file=request.FILES['other_file'],
                    #duration=duration
                )
            else:
                video = Video(
                    title=serializer.data['title'],
                    content=serializer.data['content'],
                    video_file=request.FILES['video_file'],
                    #duration=duration
                )
            video.save()
            duration = video.get_length()
            video.duration = duration
            video.save()
            try:
                if 'video_config_file' in request.FILES:
                    import_quiz_camtasia8(request.FILES['video_config_file'], video)

                concept.playlist = typed_playlist.append(video.id, concept.playlist, 0)
                concept.videos.add(video)
                concept.save()
                return Response(VideoSerializer(video).data)
            except Exception, e:
                print "Camtasia 8 exception : " + str(e)
                video.delete()
                return Response({"error": "Cannot parse Config File"}, status.HTTP_400_BAD_REQUEST)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], permission_classes=((IsOwnerOrReadOnly, )))
    def add_element(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        concept.playlist.append()
        return Response(ConceptSerializer(concept))

    def remove_video(self, concept, id):
        concept.videos.remove(Video.objects.get(pk=id))

    def remove_quiz(self, concept, id):
        concept.quizzes.remove(Quiz.objects.get(pk=id))

    def remove_document(self, concept, id):
        concept.pages.remove(Document.objects.get(pk=id))

    @action(methods=['POST'], permission_classes=((IsOwnerOrReadOnly, )))
    def delete_element(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        _id = int(request.DATA['id'])
        _type = int(request.DATA['type'])
        print "old playlist was : ", concept.playlist
        print "will delete ", _id, " ", _type
        new_playlist = typed_playlist.delete(concept.playlist, _id, _type)
        print "new plalist is : ", new_playlist
        if new_playlist is not False:
            concept.playlist = new_playlist
            if _type == 0:
                self.remove_video(concept, _id)
            elif _type == 1:
                self.remove_quiz(concept, _id)
            elif _type == 2:
                self.remove_document(concept, _id)
            concept.save()
        return Response(ConceptSerializer(concept).data)

    @action(methods=['POST'],
            permission_classes=((IsOwnerOrReadOnly, )),
            serializer_class=QuizSerializer)
    def add_quiz(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        serializer = AddQuizSerializer(data=request.DATA)
        if serializer.is_valid():
            quiz = Quiz(
                title=serializer.data['title'])
            quiz.save()
            concept.playlist = typed_playlist.append(quiz.id, concept.playlist, 1)
            concept.quizzes.add(quiz)
            concept.save()
            return Response(QuizSerializer(quiz).data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'])
    def add_existing_quiz(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        quiz = get_object_or_404(Quiz, int(request.DATA['pk']))
        concept.playlist = typed_playlist.append(quiz.id, concept.playlist, 1)
        concept.quizzes.add(quiz)
        concept.save()
        return Response(ConceptSerializer(concept).data)

    @action(methods=['POST'],
            permission_classes=((IsOwnerOrReadOnly, )),
            serializer_class=DocumentSerializer)
    def add_document(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        serializer = DocumentSerializer(data=request.DATA)
        if serializer.is_valid():
            document = Document(
                title=serializer.data['title'],
                description=serializer.data['description']
                )
            document.save()
            concept.playlist = typed_playlist.append(document.id, concept.playlist, 2)
            concept.pages.add(document)
            concept.save()
            return Response(document.to_dict())
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    #  TODO: check if the document is not already added in the concept
    @action(methods=['POST'], permission_classes=((IsOwnerOrReadOnly, )))
    def add_existing_document(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        document = get_object_or_404(Document, int(request.DATA['pk']))
        concept.playlist = typed_playlist.append(document.id, concept.playlist, 2)
        concept.pages.add(document)
        concept.save()
        return Response(ConceptSerializer(concept).data)

    # TODO: Test whether this function works correctly
    @link()
    def quizzes(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request=request, obj=concept.group.course)
        serializer = QuizSerializer(concept.quizzes.all(), many=True)
        _playlist = typed_playlist.to_array(concept.playlist)
        ordered_data = []
        for elem in _playlist:
            if elem[2] == 1:
                ordered_data.append(serializer.data[elem[1]])
        return Response(ordered_data)

    @link(permission_classes=((IsOwnerOrReadOnly, )))
    def get_concept_page_data(self, request, pk=None):
        concept = get_object_or_404(Concept, pk=pk)
        self.check_object_permissions(request, concept.group.course)
        isOwnerObj = IsOwner()
        inInstructorOrContentDeveloperModeObj = InInstructorOrContentDeveloperMode()
        if not inInstructorOrContentDeveloperModeObj.has_permission(request, None):
            if (not concept.is_published and
                    not isOwnerObj.has_object_permission(request=request,
                                                         view=None, obj=concept.group.course)):
                return Response({"error": "Concept does not exist"}, status.HTTP_400_BAD_REQUEST)
        data = {}
        data['id'] = concept.id
        data['title'] = concept.title
        data['description'] = concept.description
        data['title_document'] = concept.title_document.to_dict()
        if concept.image:
            data['image'] = concept.image.url
        else:
            data['image'] = DEFAULT_CONCEPT_IMAGE

        group = Group.objects.filter(id=concept.group_id)[0]
        course1 = Course.objects.filter(id=group.course_id)[0]

        data['group'] = group.id
        data['group_title'] = group.title
        data['course'] = course1.id
        data['course_title'] = course1.title

        data['group_playlist'] = []

        for id1 in json.loads(group.playlist):
            concept = Concept.objects.get(id=id1[0])
            if concept.is_published:
                data['group_playlist'].append({
                    'id': id1[0],
                    'title': concept.title
                })

        course_playlist = [
            {
                'id': id_pair[0],
                'title': Group.objects.filter(id=id_pair[0])[0].title
            } for id_pair in
            json.loads(course1.playlist)
        ]
        # course_playlist = [grp for grp in course_playlist if grp.is_published]
        data['course_playlist'] = course_playlist
        data['playlist'] = self.playlist_as_array(request, pk, True)
        data['current_element'] = int(request.GET.get('item', 0))
        return Response(data)
