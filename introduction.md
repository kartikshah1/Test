Prequisites for Ubuntu:
---
1. Create a user with username grader on your system. Login into this user.
2. Clone this repository.
3. run `bash install.sh`. This file installs all the needed software.
4. Now the needed software have been installed in the venv/ folder. To run the server follow the steps given below.


Setting Up development server on ubuntu:
---
1. Create database. Follow the steps given below.
    * Run 'mysql -u root -p' on the command line. On being asked the password enter the password.
    * In the mysql prompt enter 'create database elearning_academy;'. The database is created. 
    * Now exit the mysql prompt by entering 'exit;'
2. Activate the virtual environment by running 'source ./venv/bin/activate'.
3. Run 'bash server_setup.sh'. This creates the database and the tables needed using the syncdb and the migrate features of the django framework.
4. python manage.py runserver. This creates the server at 127.0.0.1:8000

Setting up the deployment server on ubuntu:
---
Have a look at - http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/ .This link guides you through the exact steps for setting up a gunicorn server.

Some known problems:  
---
1. PIL installation might turn out to be non trivial, please refer to : http://askubuntu.com/questions/156484/how-do-i-install-python-imaging-library-pil
2. For installing mysql-python you need to install python-dev.
3. OperationalError: (2003, "Can't connect to MySQL server on 10.102.56.95") [10.102.56.95 is my IP]: Edit /etc/mysql/my.cnf 'bind-address' to '10.102.56.95'

System:  
---
Django on MySQL qith Jquery and React.js for frontend. Video.js to manage HTML5 Video tag

Website serves for 3 kind of users:-
---
1.  Content Developers
2.  Instructors
3.  Students


Features supported for
---
1.  Content Developer
    * Create a Textbook course which can be used by instructors as reference
    * Offer a public course as instructor - similar to coursera or udacity
    * Enrol a course and learn like a student
    * Creating Course includes:-

        1.  Upload videos and quizes within the video
        2.  Make Quizzes and exercises to supplement a ceoncept
        3.  Upload slides and add text documents (lecture scribs)

2.  Instructor

    * Offer a course using multiple textbooks
    * Enrol a course and learn like a student
    * Offering courses includes:-

        1.  Selectively choose content from different textbook courses
        2.  Modify or Add Invideo and other quizzes
        3.  Take online exams
        4.  Provide additional documents and/or slides to supplement video

3.  Student

    * Enrol in a course
    * View Video and take quizzes
    * View performance
    * Participate in discussion forum


Modules:-
---
1.  User
2.  Notification System
3.  Discussion Forum
4.  Course
5.  Concept
6.  Quiz
7.  Video
8.  Document


Brief Description :-
---
User
============================
Every one registers as a student. Based on request a user can be upgraded to instructor
or content developer by admin (DBA as of now).
User has a rich profile associated with it, displaying his educational/professional details

Notification System :-
============================
Email Notification System to send out emails for account activation, forget password
or course welcome messages. Messages can be formatted by functions based on the service
which is using notification and sent out to single or multiple people.
Message Queue and cron jobs need to be implemented for background support and maintining
 outbox

Discussion Forum :-
============================
Forum for a course with subscription and moderation. Industry standard comment and post
mechanism equivalent to Facebook wall post and comments.

Course :-
============================
Course can be created in a category which is in a parent_category. It allows to add group
of concepts. One can moniter forum, student progress, course wiki as default pages associated
with the course.
Additional pages can be added based on instructor requirement eg Installation instruction,
pre-req etc.

Concept :-
=============================
Each course is a collection of concept. Concept is made up of a playlist of learning element.
Currently quiz, video, document are supported learning elements. Content Developer/Instructor
can add new learning elements, change order and delete elements from the concept.
Concept shows a easy to navigate view of all such elements.
Also a brief write up about the concept can be added as part of concept description.

Quiz :-
==============================
In-Video Quizzes and external Quizzes can be added. Feature to directly extract Camatia 8
quizzes from the video is provided. Three type of questions can be added - Single choice correct, Multiple choice correct, Fixed answer. Quiz can be attempted multiple time and
penalty for the same can be added by instructor.

Video :-
===============================
Video with subtitle can be added to a concept. It is played using HTML5 video element
through video.js. More customized JS will be written for better performance.
Section Markers and Quiz Markers can be added by instructor for easier navigation within
the video. A brief description specific to the video can be added as well.

Document :-
=============================
A rich text document feature with sections, headings, paragraphs and other formattings
be added to a concept. Concept can have multiple documents associated with it.
They can be lecture scribe, additional notes or any information that content developer/
instructor wants to supply to student.
