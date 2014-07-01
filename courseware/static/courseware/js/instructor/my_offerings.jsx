/** @jsx React.DOM */

/** Author : Shrikant Nagori, Alankar Saxena
**/

var CourseCreate = React.createClass({
    base_url: "/courseware/api/",

    getInitialState: function() {
        return {
            category: undefined
        };
    },

    handleCategoryChange: function(category) {
        oldState = this.state;
        oldState.category = category;
        this.setState(oldState)
    },

    add_course: function() {
        url = this.base_url + "offering/?format=json";
        var fd = new FormData();
        fd.append('category', this.state.category);
        fd.append('title', this.refs.title.getDOMNode().value.trim());
        if(this.refs.image.getDOMNode().files[0]){
            fd.append('image', this.refs.image.getDOMNode().files[0]);
        }
        request = ajax_custom_request({
            url: url,
            type: "POST",
            data: fd,
            mimeType: 'multipart/form-data',
        });
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            window.location = "/courseware/course/" + response.id;
        }.bind(this));
        return false;
    },

    render: function() {
            return (
                <form id="addcourse" role="form" class="form-horizontal" enctype="multipart/form-data" ref="courseForm">
                    <fieldset>
                    <CategoryLoader callback={this.handleCategoryChange} />
                    <div class="form-group">
                        <label class="control-label col-md-2 col-md-offset-1">Title</label>
                        <div class="col-md-7 col-md-offset-1">
                            <input name="title" type="text" class="form-control" ref="title" placeholder="Title"></input>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-2 col-md-offset-1">Course Image</label>
                        <div class="col-md-7 col-md-offset-1">
                            <input name="image" type="file" class="form-control" ref="image"></input>
                            <p class="help-block">Some Help Text </p>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-2 col-md-offset-1">Enrollment Type</label>
                        <div class="col-md-7 col-md-offset-1">
                            <select ref="enrollment_type" name="enrollment_type" class="form-control">
                                <option value="O">Open</option>
                                <option value="M">Moderated</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-md-2 col-md-offset-2  addcoursebutton">
                            <button ref="submit" class="btn btn-primary" type="button" onClick={this.add_course}>Add Offering</button>
                        </div>
                        <div class="col-md-1">
                            <button type="button" onClick={this.props.closeCallBack} class="btn btn-danger">
                                Close
                            </button>
                        </div>
                    </div>
                    </fieldset>
                </form>
            );
        }
});


var AddCourseForm = React.createClass({

    closeCallBack: function() {
        this.props.closeCallBack;
    },

    render: function() {
        console.log("AddCourseForm");
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    Add Offering
                    <span class="pull-right">
                        <button type="button" onClick={this.props.closeCallBack} class="close">&times;</button>
                    </span>
                </div>
                <div class="panel-body">
                    <CourseCreate closeCallBack={this.props.closeCallBack}/>
                </div>
            </div>
        );
    }
});


var Concept = React.createClass({

    loadConcepts: function() {
        url = "/courseware/api/course/"+this.props.courseid+"/groups/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.setState({concepts: response, loaded: true});
        }.bind(this));
    },

    getInitialState: function() {
        return {
            loaded: false,
            concepts: undefined
        };
    },

    componentDidMount: function() {
        this.loadConcepts();
    },

    render: function(){
        if(!this.state.loaded) {
            return (
                <LoadingBar />
            );
        }
        else {
            var concept = this.state.concepts.map(
                function (concept_name) {
                    return <div class = "conceptname"> {concept_name.title} </div>;
            }.bind(this));
            return (
                <div>
                    {concept}
                </div>
            );
        }
    }

});

var Course = React.createClass({

    deleteCourse: function(){
        url = "/courseware/api/course/" + this.props.course.id;
        request = ajax_json_request(url, "DELETE", {});
        request.done(function(response) {
            display_global_message("The course was successfully deleted", "success");
            $("#" + "course" + this.props.course.id).remove();
        }.bind(this));
        request.complete(function(response) {
            console.log("ss")
            if (response.status != 200) {
                display_global_message("The course could not be deleted", "error");
            }
        }.bind(this));
    },

    setProgress: function() {
        course = this.props.course;
        var div = document.getElementById("pgbar" + course.id);
        div.style.width = course.progress + "%";
    },

    showDelete: function(){
        course = this.props.course;
        if(course.is_published === true){
            var div = document.getElementById("delete" + course.id);
            div.style.visibility = 'hidden';
        }
    },

    handleClicks: function(event){
        element = $(event.target);
        console.log(element);
        id = element.context.id;
        console.log(id);
        if(id == "-1") {
            window.location.href = "/courseware/course/" + this.props.course.id;
        }
        else if(id == "-2"){
           window.location.href = "/courseware/course/" + this.props.course.id + "/-8";
        }
        else if(id == "-3") {
            //window.location.href = "/courseware/course/" + this.props.course.id + "/syllabus";
        }
        else if(id == "-4"){
            window.location.href = "/courseware/course/" + this.props.course.id;
        }
        else{

        }
   },

    componentDidMount: function() {
        this.setProgress();
        this.showDelete();
        $( "#accordion" ).accordion({
            animate: 100,
            collapsible: true,
            heightStyle: "content"
        });
    },

    render: function(){
        course = this.props.course;
        var progress = course.progress + "%"
        var url = "/courseware/course/" + course.id;
        var pgbarid = "pgbar" + course.id;
        var start_msg = "";
        var button_msg = "";
        var label = "label" + course.id;
        var modal = "modal" + course.id;
        var mymodal = "#" + modal;
        var courseid = "course" + course.id;
        /** Only courses which have is_published = false would be shown the delele option **/
        var deletediv = "delete" + course.id;

        if(course.coursetag == 1){
            start_msg = "Course Started : " + course.start_date;
            button_msg = "Take Class";
        }
        else if(course.coursetag == 2){
            start_msg = "Course Starts : " + course.start_date;
            button_msg = "Prepare Class";
        }
        else {
            start_msg = "Course Ended : " + course.end_date;
            button_msg = "Take a tour";
        }
        var concepts = function () {
                    return <Concept courseid={course.id} />;
            }.bind(this);
        return  (<li id={courseid} class = "myofferingBox">
                <div >
                    <div class = "header row" >
                        <CourseDeleteModal label={label} modal={modal} title={course.title} callback={this.deleteCourse} />
                        <div class = "col-md-5 myofferingHeading">
                             IIT BOMBAY
                        </div>
                        <div class = "col-md-6">
                            <div class = "myofferingDate">
                                {start_msg}
                            </div>
                        </div>
                        <div id={deletediv} class = "col-md-1 myofferingDate">
                            <a data-toggle="modal" href={mymodal}>
                                <span class="glyphicon glyphicon-trash icon"></span>
                            </a>
                        </div>

                    </div>
                    <div class = "row myofferingTitle">
                        <a  onClick ={this.handleClicks} id="-1"> {course.title}
                        </a>
                    </div>
                    <div class = "row myofferingActions">
                        <div class = "col-md-1 myschedule mycourseLink">
                            <a onClick ={this.handleClicks} id="-2"> Settings </a>
                        </div>
                        <div class = "col-md-1 mycourseLink">
                            <a onClick ={this.handleClicks} id="-3"> Syllabus
                            </a>
                        </div>
                        <div class = "col-md-2 col-md-offset-1">
                            <a onClick ={this.handleClicks} id="-4" class="btn btn-primary tool-tip mybtn">
                                {button_msg}
                            </a>
                        </div>
                        <div class = "col-md-5">
                            <div  class = "mycourseProgress">
                                Course Progress
                            </div>
                            <div class="progress progress-striped  pgdiv">
                                <div id = {pgbarid} class="progress-bar pgbar" role="progressbar"
                                    aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div class = "row detailsrow">
                        <div class = "myconcepts col-md-5">
                            <div class = "concepts">
                                Groups
                            </div>
                            <div class = "conceptbox">
                                {concepts()}
                            </div>
                        </div>
                        <div class = "myofferingDetails col-md-5 col-md-offset-2">
                                <div >
                                    <span class="glyphicon glyphicon-user"></span>
                                    <a class = "detaillink"
                                        href={"/courseware/course/" + this.props.course.id + "/-6"}>
                                        Students </a>
                                </div>
                                <div>
                                    <span class="glyphicon glyphicon-envelope"></span>
                                    <a class = "detaillink"  href= "" > News Feed
                                    </a>
                                </div>
                                <div>
                                     <span class="glyphicon glyphicon-globe"></span>
                                      <a class = "detaillink"  href= {"/courseware/course/" + this.props.course.id + "/-3"} > Discussion Forum
                                    </a>
                                </div>
                                <div>
                                    <span class="glyphicon glyphicon-book"></span>
                                    <a class = "detaillink"  href= {"/courseware/course/" + this.props.course.id + "/-4"} > Wiki
                                    </a>
                                </div>
                        </div>
                    </div>
                </div>
                </li>
            );
    }
});


var MyCourseBody = React.createClass({

    getInitialState: function() {
        return {
            loaded: false,
            showform: false,
        };
    },

    addcourseform: function() {
        oldState = this.state;
        oldState['showform'] = true;
        this.setState(oldState);
    },

    closePanel: function() {
        oldState = this.state;
        oldState['showform'] = false;
        this.setState(oldState);
    },

    componentDidMount: function() {
        if (document.contains($("#accordion"))) {
            $("#accordion").accordion("destroy");
            $( "#accordion" ).accordion({
                    animate: 100,
                    collapsible: true,
                    heightStyle: "content"
                });
        }
    },

    render: function() {
        courses = jQuery.parseJSON(this.props.courses);

        console.log(courses);
        var addcourseform =<div></div>
        if(this.state.showform) {
            addcourseform = <AddCourseForm closeCallBack={this.closePanel}/>;
        }
        if(courses == ""){
            courses = (<div class="alert alert-danger alert-dismissable">No courses offered yet</div>);
        }
        else{
            var courses = courses.map(
                function (course) {
                    return <Course course={course} />;
            }.bind(this));
        }
        return (<div>
                    <div id="courseBar" class="row coursebar">
                        <div class="col-md-8 offeringTitle offeringTitlemessage">
                            MY OFFERINGS
                        </div>
                         <div class="col-md-4 offeringTitle ">
                            <button class="btn btn-primary addcourse-button pull-right" onClick={this.addcourseform}>
                                <span class="glyphicon glyphicon-plus-sign"></span>
                                &nbsp;&nbsp;Add Offering
                            </button>
                        </div>
                    </div>
                    <div class = "courseContainer">
                        <div>
                            <div id="addcourseform">
                                {addcourseform}
                            </div>
                            <ul id="accordion">
                                {courses}
                            </ul>
                        </div>
                    </div>
                </div>
        );
    }
});
