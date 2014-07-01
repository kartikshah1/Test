"""
Views for Video

TODO
    - import quiz from the camtasia xml file into our database

Video API :-
    Since Video is always a part of some concept and does not exist standalone
    so the add and remove functionality are part of Concept API.

    Support following actions :-
    1.  Update Title (Cannot be empty)
    2.  Edit content
    3.  Add Marker
    4.  Delete Marker
    5.  Update Marker

"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.forms import ModelForm

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from video.models import Video, VideoHistory, Marker, QuizMarker, SectionMarker
from video.serializers import VideoSerializer, AddVideoSerializer
from video.serializers import MarkerSerializer, SectionMarkerSerializer, QuizMarkerSerializer

from quiz.models import Quiz, QuestionModule, DescriptiveQuestion
from quiz.models import SingleChoiceQuestion, FixedAnswerQuestion

import math
import json
import xml.etree.ElementTree as ET


def import_quiz_camtasia8(con_file, video):
    """
    Doc
    """
    #tree = ET.parse(fname)
    tree = ET.fromstring(con_file.read())
    rdf = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
    tscIQ = '{http://www.techsmith.com/xmp/tscIQ/}'
    xmpDM = '{http://ns.adobe.com/xmp/1.0/DynamicMedia/}'
    quiz_xpath = ".//" + rdf + "Description[@" + tscIQ + "questionSetName]"

    for quiz in tree.findall(quiz_xpath):
        title = quiz.attrib[tscIQ + "questionSetName"]
        startTime = int(math.floor(float(quiz.attrib[xmpDM + "startTime"])/1000))
        question_xpath = ".//" + rdf + "Description[@" + tscIQ + "id]"

        quiz_obj = Quiz(title=title)
        quiz_obj.save()
        try:
            marker = QuizMarker(video=video, time=startTime, quiz=quiz_obj)
            marker.save()
            qmodule_obj = QuestionModule(
                title='Dummy Title',
                quiz=quiz_obj,
                dummy=True
            )
            qmodule_obj.save()

        except Exception, e:
            quiz_obj.delete()

            try:
                marker = QuizMarker.objects.get(video=video, time=startTime)
                quiz_obj = marker.quiz
                qmodule_obj = QuestionModule.objects.filter(quiz=quiz_obj)[0]
                if(qmodule_obj.dummy):
                    qmodule_obj.dummy = False
                    qmodule_obj.title = quiz_obj.title
                    qmodule_obj.save()
                    quiz_obj.title = "Quiz : Multiple Questions"
                    quiz_obj.save()
                qmodule_obj = QuestionModule(
                    title=title,
                    quiz=quiz_obj,
                    dummy=False
                )
                qmodule_obj.save()

            except Exception,e:
                marker = None
                print "Some other error in marker creation at %d, %d" %(startTime, video.id)
                print(e)


        for question in quiz.findall(question_xpath):
            qtype = question.attrib[tscIQ + 'type']
            qtext = question[0].text
            if qtype == 'MC':
                # print "multiple choice"
                # answer_xpath = ".//" + tscIQ + "correctAnswer"
                answer = int(math.log(int(question[1].text), 2))
                options = json.dumps(
                    [opt.text for opt in
                        question.findall(".//" + tscIQ + "answer")]
                )
                q = SingleChoiceQuestion(
                    quiz=quiz_obj, question_module=qmodule_obj,
                    description=qtext, options=options, answer=answer, marks=1
                )
                q.save()
            elif qtype == 'FITB':
                # print "fixed answer"
                answer = json.dumps(
                    [ans.text for ans in
                        question.findall(".//" + tscIQ + "answer")]
                )
                q = FixedAnswerQuestion(
                    quiz=quiz_obj, question_module=qmodule_obj,
                    description=qtext, answer=answer, marks=0
                )
                q.save()
            elif qtype == 'SHORT':
                # print "descriptive"
                q = DescriptiveQuestion(
                    quiz=quiz_obj, question_module=qmodule_obj,
                    description=qtext, answer="Enter Answer Here"
                )
                q.save()
            else:
                raise Exception("Unknown Question Type")

    namespace = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'tscIQ': "http://www.techsmith.com/xmp/tscIQ/",
        'xmpDM': "http://ns.adobe.com/xmp/1.0/DynamicMedia/",
    }
    s_xpath = ".//rdf:Description[@xmpDM:trackType='TableOfContents']//rdf:Description"
    name_attrib = "{" + namespace['xmpDM'] + "}name"
    time_attrib = "{" + namespace['xmpDM'] + "}startTime"
    for section in tree.findall(s_xpath, namespaces=namespace):
        title = section.attrib[name_attrib]
        if ("quiz" not in title.lower()):
            start_time = int(math.ceil(float(section.attrib[time_attrib])/1000))
            print title, start_time
            marker = SectionMarker(video=video, time=start_time, title=title)
            try:
                marker.save()
            except Exception, err:
                print "marker repeated at %d for video %d - type Section" % (start_time, video.id)
                print str(err)



class MarkerViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
        Marker for a video is created/updated/delete after checking the user has permission
        to add marker to the video.
    """
    #permission_classes = (IsVideoOwner, )

    model = Marker
    serializer_class = MarkerSerializer

    def create(self, request):
        """
            Create a Marker based on type in request.DATA
        """
        print "Create Marker"
        if request.DATA['type'] == Marker.SECTION_MARKER:
            serializer = SectionMarkerSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                markers = []
                for m in serializer.object.video.markers.all():
                    sub_m = Marker.objects.filter(pk=m.id).select_subclasses()[0]
                    if m.type == 'S':
                        markers.append(SectionMarkerSerializer(sub_m).data)
                    else:
                        markers.append(QuizMarkerSerializer(sub_m).data)
                response = {'markers': markers}
                return Response(response, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        elif request.DATA['type'] == Marker.QUIZ_MARKER:
            serializer = QuizMarkerSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                markers = []
                for m in serializer.object.video.markers.all():
                    sub_m = Marker.objects.filter(pk=m.id).select_subclasses()[0]
                    if m.type == 'S':
                        markers.append(SectionMarkerSerializer(sub_m).data)
                    else:
                        markers.append(QuizMarkerSerializer(sub_m).data)
                response = {'markers': markers}
                return Response(response, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Bad Type for Marker", status.HTTP_400_BAD_REQUEST)

    #def update(self, request, pk=None):
    #    """
    #        Marker is never updated completely rather only partially
    #    """
    #    return Response("Update should not be called", status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
            Update a Marker based on instance of Marker class
        """
        marker = get_object_or_404(Marker, pk=pk)
        sub_marker = Marker.objects.filter(pk=pk).select_subclasses()[0]
        if (marker.type == Marker.SECTION_MARKER):
            serializer = SectionMarkerSerializer(sub_marker, data=request.DATA, partial=True)
            if serializer.is_valid():
                serializer.save()
                markers = []
                for m in sub_marker.video.markers.all():
                    sub_m = Marker.objects.filter(pk=m.id).select_subclasses()[0]
                    if m.type == 'S':
                        markers.append(SectionMarkerSerializer(sub_m).data)
                    else:
                        markers.append(QuizMarkerSerializer(sub_m).data)
                response = {'markers': markers}
                return Response(response, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        elif marker.type == Marker.QUIZ_MARKER:
            serializer = QuizMarkerSerializer(sub_marker, data=request.DATA, partial=True)
            if serializer.is_valid():
                serializer.save()
                markers = []
                for m in sub_marker.video.markers.all():
                    sub_m = Marker.objects.filter(pk=m.id).select_subclasses()[0]
                    if m.type == 'S':
                        markers.append(SectionMarkerSerializer(sub_m).data)
                    else:
                        markers.append(QuizMarkerSerializer(sub_m).data)
                response = {'markers': markers}
                return Response(response, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            return("Unknown Marker type", status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
            Destroy Marker
        """
        marker = get_object_or_404(Marker, pk=pk)
        video = marker.video
        marker.delete()
        markers = []
        for m in video.markers.all():
            sub_m = Marker.objects.filter(pk=m.id).select_subclasses()[0]
            if m.type == 'S':
                markers.append(SectionMarkerSerializer(sub_m).data)
            else:
                markers.append(QuizMarkerSerializer(sub_m).data)
        response = {'markers': markers}
        return Response(response, status.HTTP_200_OK)


class VideoViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
        Video can be added only from a concept by content developer.
        Videos can be removed from concept-video relationships. When a video
        is not referenced by any concept then the video should be deleted
        by a Garbage collection tool.

        We allow :-
        1. Get Video
        2. Update Video (Title, Content)
        3. Upvote/Downvote
    """

    model = Video
    serializer_class = VideoSerializer

    def update(self, request, pk=None, **kwargs):
        """
            Update and existing video. You can only partially update an existing video
        """
        if (request.FILES.has_key('video_file')):
            return Response({"msg": "Video File cannot be changed"}, status.HTTP_400_BAD_REQUEST)
        return super(VideoViewSet, self).update(request, pk, **kwargs)

    def partial_update(self, request, pk=None, **kwargs):
        """
            Update the title and content of video
        """
        if ('other_file' in request.FILES):
            video = get_object_or_404(Video, pk=pk)
            video.other_file = request.FILES['other_file']
            video.save()
        if (request.FILES.has_key('video_file')):
            return Response({"msg": "Video File cannot be changed"}, status.HTTP_400_BAD_REQUEST)
        return super(VideoViewSet, self).partial_update(request, pk, **kwargs)
#        video = get_object_or_404(Video, pk=pk)
#        serializer = AddVideoSerializer(video, data=request.DATA, partial=True)
#        if serializer.is_valid():
#            serializer.save()
#            return Response("Video Updated", status.HTTP_200_OK)
#        else:
#            content = serializer.errors
#            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'patch'])
    def vote(self, request, pk=None):
        """
            Upvote for video
        """
        video = get_object_or_404(Video, pk=pk)
        user = request.user
        video_history = get_object_or_404(VideoHistory, video=video, user=user)

        if request.DATA['vote'] == 'up':
            if video_history.vote == VideoHistory.UPVOTE:
                video.upvotes = video.upvotes - 1
                video.save()
                video_history.vote = VideoHistory.NOVOTE
                video_history.save()
            elif video_history.vote == VideoHistory.DOWNVOTE:
                video.downvotes = video.downvotes - 1
                video.upvotes = video.upvotes + 1
                video.save()
                video_history.vote = VideoHistory.UPVOTE
                video_history.save()
            elif video_history.vote == VideoHistory.NOVOTE:
                video.upvotes = video.upvotes + 1
                video.save()
                video_history.vote = VideoHistory.UPVOTE
                video_history.save()

        elif request.DATA['vote'] == 'down':
            if video_history.vote == VideoHistory.DOWNVOTE:
                video.downvotes = video.downvotes - 1
                video.save()
                video_history.vote = VideoHistory.NOVOTE
                video_history.save()
            elif video_history.vote == VideoHistory.UPVOTE:
                video.downvotes = video.downvotes + 1
                video.upvotes = video.upvotes - 1
                video.save()
                video_history.vote = VideoHistory.DOWNVOTE
                video_history.save()
            elif video_history.vote == VideoHistory.NOVOTE:
                video.downvotes = video.downvotes + 1
                video.save()
                video_history.vote = VideoHistory.DOWNVOTE
                video_history.save()
        else:
            return Response({'msg': "Bad Request"}, status.HTTP_400_BAD_REQUEST)
        video = get_object_or_404(Video, pk=pk)
        return Response({'vote': [video.upvotes, video.downvotes]}, status.HTTP_200_OK)


@login_required
def play_video(request):
    return render(request, "video/play_video.html")


@login_required
def edit_video(request):
    return render(request, "video/edit_video.html")


class UploadVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'content', 'video_file']


@login_required
def upload_video(request):
    print("came here")
    if request.method == 'POST':
        form = UploadVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'video/edit_video.html')
        else:
            print("incorrect form")
            form = UploadVideoForm()
            return render(request, 'video/upload_video.html', {'form': form})
    else:
        form = UploadVideoForm()
        return render(request, 'video/upload_video.html', {'form': form})
