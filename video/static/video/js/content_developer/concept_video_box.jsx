/** @jsx React.DOM */


/**
    Concept Video Box for content developer or instructor.
    This will be rendered in content_developer_concept.jsx
    Provides features to :-
        1.  Add Markers
        2.  Edit Markers
        3.  Edit Video detail (title and description)

    ToDo :-
        1.  Error display on wrong/invalid form input
        2.  Functionality to add and edit quiz on a marker
**/


/**
    ConceptVideoBox [R]
        -   Video Navigation { Serves Student more }
        -   VideoTOC [R]
        -   VideoVote [R]
        -   Video [R]
        -   MarkerArea [R]
**/
var ConceptVideoBox = React.createClass({
    mixins: [ScrollToElementMixin],

    updateMarker: function(markers) {
        state = this.state;
        state.markers = markers;
        state.current_marker = 0;
        this.setState(state);
    },

    changeTitle: function(title, content) {
        state = this.state;
        state.title = title;
        state.content = content;
        this.setState(state)
    },

    changeCurrent: function(index) {
        if (index == -2) {
            if (this.state.markers.length == 0) {
                index = -1;
            } else {
                index = 0;
            }
        }
        start_time = 0;
        if (index >= 0 && this.state.markers.length >= 0) {
            start_time = this.state.markers[index]['time'];
        }
        state = this.state;
        state.current_marker = index;
        state.startTime = start_time;
        this.setState(state);
    },

    getInitialState: function() {
        data = this.props.data;
        cur_marker = 0;
        if (data.content.markers.length == 0) {
            cur_marker = -1;
        }
        return {
            title: data.content.title,
            content: data.content.content,
            current_marker: cur_marker,
            markers: data.content.markers,
            startTime: 0,
            videoLength: data.content.duration,
        };
    },

    render: function() {
        data = this.props.data;
        console.log("Concept Video box state :- ");
        console.log(this.state);
        marker = undefined;
        if (this.current_marker != -1) {
            marker = this.state.markers[this.state.current_marker];
        } else {
            marker = undefined;
        }
        if (this.state.videoLength) {
            marker_area = <MarkerArea videoId={data.content.id} videoLength={this.state.videoLength}
                         marker={marker} updateMarkerCallback={this.updateMarker} cancelAdd={this.changeCurrent}/>;
        } else {
            marker_area = <LoadingBar />
        }
        return (
            <div class="row" class="concept-video-box">
                <div class="col-md-4 panel-group video-sidebar" id="video-sidebar">
                    <VideoContent content={this.state.content} videoId={data.content.id}
                        title={this.state.title} changeTitle={this.changeTitle}/>
                    <VideoTOC markers={this.state.markers} clickCallback={this.changeCurrent} />
                    <VideoSlide id={data.content.id} other_file={data.content.other_file} />
                </div>
                <div class="col-md-8 video-container" id="video-container">
                    <VideoNavigation
                        nextVideo={this.props.nextCallback}
                        prevVideo={this.props.prevCallback}
                        title={this.state.title} />
                    <Video videoFile={data.content.video_file} videoStartTime={this.state.startTime} />
                    <VideoVote upvotes={data.content.upvotes} downvotes={data.content.downvotes} />
                    {marker_area}
                </div>
            </div>
        );
    }
});

var VideoSlide = React.createClass({

    render: function() {
        console.log("props of the video are : ");
        console.log(this.props);
        return (
            <div class="panel panel-default video-desc-container" id="slide-container"
                ref="videoSlideDiv">
                <div class="panel-heading" data-toggle="collapse"
                    data-parent="#video-sidebar" data-target="#slide-description">
                    <span class="video-sidebar-heading"> Slides </span>
                </div>
                <div class="video-sidebar-content panel-collapse collapse" id="slide-description">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="video-desc">
                                <ImageUploader image={this.props.other_file}
                                url = {"/video/api/video/" + this.props.id + "/?format=json"}
                                showProgress={true}
                                name="other_file"
                                isFile={true} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});



/**
    VideoContent
        -   Content
**/
var VideoContent = React.createClass({

    base_url: "/video/api/",

    updateVideoResult: function(param) {
        alert(param['msg']);
    },

    updateVideoDetail: function() {
        new_title = this.refs.videoNewTitle.getDOMNode().value;
        new_content = this.refs.videoNewContent.getDOMNode().value;
        if (new_title == "" || new_content == "") {
            error_messages = [];
            if ( new_title == "" ){
                error_messages.push("Title cannot be empty");
                $(this.refs.videoNewTitle.getDOMNode().parentNode).addClass("has-error");
            }
            if ( new_content == "" ) {
                error_messages.push("Content cannot be empty");
                $(this.refs.videoNewContent.getDOMNode().parentNode).addClass("has-error");
            }
            this.setState({error_messages: error_messages});
        } else {
            url = this.base_url + "video/" + this.props.videoId + "/?format=json";
            data = {
                'title': new_title,
                'content': new_content
            };
            request = ajax_json_request(url, "PATCH", data);
            request.done(function(response) {
                //response = jQuery.parseJSON(response);
                this.updateVideoResult({'error': false, 'msg': "Video Detail Updated Succesfully"});
                this.props.changeTitle(new_title, new_content);
                if ($(this.refs.videoNewTitle.getDOMNode().parentNode).hasClass("has-error")) {
                    $(this.refs.videoNewTitle.getDOMNode().parentNode).removeClass("has-error");
                }
                if ($(this.refs.videoNewContent.getDOMNode().parentNode).hasClass("has-error")) {
                    $(this.refs.videoNewContent.getDOMNode().parentNode).removeClass("has-error");
                }
                this.setState({error_messages: []})
            }.bind(this));
            request.fail(function(response) {
                this.updateVideoResult({'error': true, 'msg': "Video Update Failed. Try Later"});
                //$($(this.refs.videoNewTitle.getDOMNode()).parentNode).addClass("has-error");
                //$($(this.refs.videoNewContent.getDOMNode()).parentNode).addClass("has-error");
            }.bind(this));
        }
    },

    editVideoToggle: function() {
        state = this.state;
        state.edit = ! state.edit;
        state.error_messages = [];
        this.setState(state);
    },

    getInitialState: function(){
        return {
            edit: false,
            title: this.props.title,
            content: this.props.content,
            error_messages: [],
        };
    },

    componentWillReceiveProps: function(nextProps) {
        state = this.state;
        state.title = nextProps.title;
        state.content = nextProps.content;
        state.edit = false;
        this.setState(state);
    },

    render: function() {
        videoInnerContent = null;
        if (this.state.edit == false) {
            videoInnerContent = <div class="video-desc">
                                    <h4> {this.state.title} </h4>
                                    <p> {this.state.content} </p>
                                </div>;
            button =  <div class="video-sidebar-btn-grp">
                                <a class="pull-right btn btn-primary" href="#" onClick={this.editVideoToggle}>
                                    Edit </a>
                            </div>;
            error = undefined;
        }else {
            button =  <div class="video-sidebar-btn-grp">
                                <a class="pull-left btn btn-success" href="#" onClick={this.updateVideoDetail}>
                                    Update </a>
                                <a class="pull-right btn btn-danger" href="#" onClick={this.editVideoToggle}>
                                    Cancel </a>
                            </div>;
            videoInnerContent = <form class="video-desc-form">
                                <div>
                                    <input name="video-title" type="text" ref="videoNewTitle" class="form-control"
                                    placeholder="Video Title" defaultValue={this.state.title}/>
                                </div>
                                <div class="wmd-toolbox"></div>
                                <div>
                                    <WmdTextarea name="video-content" ref="videoNewContent" style={{height: '150px'}}
                                    placeholder="Video Description" defaultValue={this.state.content} />
                                </div>
                                </form>;
            error_messages = this.state.error_messages.map( function(error, index) {
                return <li class="form-error-msg"> {error} </li>;
            });
            error = undefined;
            if (error_messages.length > 0) {
                error = <div class="row">
                            <div class="col-md-12">
                                <ul class="form-error alert alert-danger">
                                    {error_messages}
                                </ul>
                            </div>
                        </div>;
            }
        }
        return (
            <div class="panel panel-default video-desc-container" id="content-container" ref="videoContentDiv">
                <div class="panel-heading" data-toggle="collapse"
                    data-parent="#video-sidebar" data-target="#video-description">
                    <span class="video-sidebar-heading"> Description </span>
                </div>
                <div class="video-sidebar-content panel-collapse collapse in" id="video-description">
                    {error}
                    <div class="row">
                        <div class="col-md-12 video-sidebar-btn-grp">
                            {button}
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            {videoInnerContent}
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});


/**
    VideoTOC
        -   Video Title
        -   Video Description
        -   Video Markers
**/
var VideoTOC = React.createClass({

    addMarker: function() {
        $("#toc").addClass("in");
        $("#toc").css({"height": "auto"});
        $("#toc").removeClass("collapse");
        $("#toc-heading").removeClass("collapsed");
        this.props.clickCallback(-1);
        return false;
    },

    handleClick: function(index) {
        this.props.clickCallback(index);
        return false;
    },

    toTime: function(t) {
            sec = t%60;
            min = (t-sec)/60;
            if (sec < 10) {
                sec = "0"+sec;
            }
            if (min < 10) {
                min = "0"+min;
            }
            return min + ":" + sec;
    },

    render: function() {
        var markers = this.props.markers.map(
                function (marker, index) {
                    if (marker.type == 'S') {
                        return <li key={index} id={"marker_"+marker.id} class="marker-item"
                                    href="#" onClick={this.handleClick.bind(this, index)}>
                                    <span href="#" class="marker-title">
                                        {marker.title}
                                    </span>
                                    <span class="marker-time">
                                        {this.toTime(marker.time)}
                                    </span>
                                </li>;
                    } else {
                        return <li key={index} id={"marker_"+marker.id} class="marker-item"
                                    href="#" onClick={this.handleClick.bind(this, index)}>
                                    <span href="#" class="marker-title">
                                        Quiz
                                    </span>
                                    <span class="marker-time">
                                        {this.toTime(marker.time)}
                                    </span>
                                </li>;
                    }
                }.bind(this)
            );
        return (
            <div class="panel panel-default video-toc-container" id="toc-container">
                <div class="panel-heading" data-toggle="collapse" data-parent="#video-sidebar"
                    data-target="#toc" id="toc-heading">
                    <span class="video-sidebar-heading"> Table of Content </span>
                    <span class="video-sidebar-btn-grp">
                        <a class="pull-right btn btn-primary" href="#" onClick={this.addMarker}>Add Marker</a>
                    </span>
                </div>
                <div class="video-sidebar-content panel-collapse collapse" id="toc">
                    <ul id="tocList" role="menu" class="tocList">
                        {markers}
                    </ul>
                </div>
            </div>
        );
    }
});


/**
    Video Navigation
        -   Previous Video
        -   Next Video
        -   Auto Play
**/
var VideoNavigation = React.createClass({
    render: function() {
        return (
            <div class="row video-navigation" id="navigation-container">
                <span class="video-nav-btn pull-left"> <a href="#" onClick={this.props.nextVideo}>
                    <span class="glyphicon glyphicon-step-backward" />
                </a> </span>
                <span class="video-title"> {this.props.title} </span>
                <span class="video-nav-btn pull-right"> <a href="#" onClick={this.props.prevVideo}>
                    <span class="glyphicon glyphicon-step-forward" />
                </a> </span>
            </div>
        );
    }
});


/**
    Video
        -   Video Element
**/
var Video = React.createClass({

    video: undefined,

    componentWillReceiveProps: function(nextProps) {
        console.log("Video receiving props");
        videoStartTime = nextProps.videoStartTime;
        _V_("video-player").ready(function() {
            setTimeout(function(){
                video.currentTime = videoStartTime;
                video.pause();
                console.log("Return from video set time");
            }, 1);
        });
    },

    componentDidUpdate: function() {
        console.log("Video did update");
        video = document.getElementsByTagName("video")[0];
    },

    componentDidMount: function() {
        // ToDo: Setup a server side cron job to get the video duration.
        this.video = document.getElementsByTagName("video")[0];
        this.video.oncontextmenu = function() { return false; };
        video = this.video;
        _V_("video-player").ready(function() {
            setTimeout(function(){
                console.log("Video is ready");
            }, 1);
        });
        console.log("Return from video did mount");
    },

    render: function() {
        file = this.props.videoFile;
        return (
            <div class="video">
                <video ref="videoPlayer" id="video-player" class="video-js vjs-default-skin"
                    controls autobuffer preload="auto" width="720" height="480" data-setup='{}'>
                    <source type='video/webm' src={file} />
                    <source type='video/mp4' src={file} />
                    <track src="/media/static/video/a.srt" srclang="en" label="English" default />
                </video>
            </div>
        );
    }
});


/**
    VideoVote
        -   Upvote
        -   Downvote
**/
var VideoVote = React.createClass({
    render: function() {
        return (
            <div class="row video-vote">
                <span class="pull-right">
                    <span class="text-success"> <b> Upvotes </b> </span> : {this.props.upvotes}
                    <span class="text-danger"> <b> Downvotes </b> </span> : {this.props.downvotes}
                </span>
            </div>
        );
    }
});


/**
    MarkerArea
        -   Marker Title
        -   Marker Video Time ( seconds from start )
        -   Marker Type
        -   Marker Quiz (if type is QuizMarker)
**/
var MarkerArea = React.createClass({

    base_url: "/video/api/",

    deleteMarker: function() {
        url = this.base_url + "marker/" + this.props.marker.id + "/?format=json";
        request = ajax_json_request(url, "DELETE", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.updateMarkerResult({'error': false, 'msg': "Marker Deleted Succesfully"});
            this.props.updateMarkerCallback(response['markers']);
        }.bind(this));
        request.fail(function(response) {
            this.updateMarkerResult({'error': true, 'error_msg': "Could not Delete. Try Later"});
        }.bind(this));
    },

    updateMarkerResult: function(param, callback) {
        if(param.error) {
            error_messages = [];
            error_messages.push(param.msg);
            this.setState({error_messages: error_messages}, callback);
        } else {
            this.setState({error_messages: []}, callback);
        }
    },

    updateMarker: function(data) {
        url = this.base_url + "marker/" + this.props.marker.id + "/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.updateMarkerResult({'error': false, 'msg': "Marker Updated Succesfully"});
            this.props.updateMarkerCallback(response['markers']);
        }.bind(this));
        request.fail(function(response) {
            this.updateMarkerResult({'error': true, 'msg': "Update Error, Bad Input"});
        }.bind(this));
    },

    updateSectionMarker: function() {
        marker_time = $(this.refs.slider.getDOMNode()).slider("value");
        title = this.refs.title.getDOMNode().value.trim();
        if (title) {
            data = {
                'time': marker_time,
                'title': title
            };
            $(this.refs.title.getDOMNode().parentNode).removeClass("has-error");
            this.updateMarker(data);
        } else {
            addErrorClassFn = function() {
                $(this.refs.title.getDOMNode().parentNode).addClass("has-error");
            }.bind(this);
            this.updateMarkerResult(
                {'error': true, 'msg': "Marker Title required"}, addErrorClassFn);
        }
    },

    updateQuizMarker: function() {
        marker_time = $(this.refs.slider.getDOMNode()).slider("value");
        data = {
            'time': marker_time
        };
        var url = "/quiz/api/quiz/" + this.props.marker.quiz + "/?format=json";
        request = ajax_json_request(url, "PATCH", {title: this.refs.title.getDOMNode().value});
        request.done(function(new_title){
            console.log('updated title of quiz to '+ new_title);
        }.bind(this, this.refs.title.getDOMNode().value));
        this.updateMarker(data);
    },

    cancelAddMarker: function() {
        this.props.cancelAdd(-2);
    },

    postMarkerData: function(data) {
        url = this.base_url + "marker/?format=json";
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            titleParent = this.refs.title.getDOMNode().parentNode;
            removeErrorClassFn = function() {
                $(titleParent).addClass("has-error");
            };
            this.updateMarkerResult({'error': false, 'msg': "Marker Added Succesfully"}, removeErrorClassFn);
            this.props.updateMarkerCallback(response['markers']);
        }.bind(this));
        request.fail(function(response) {
            this.updateMarkerResult({'error': true, 'msg': "Add Marker Error, Bad Input"});
        }.bind(this));
    },

    createQuiz: function(title) {
        url = '/quiz/api/' + "quiz/?format=json";
        data = {
            title: title
        };
        request = ajax_json_request(url, "POST", data);
        return request;
    },

    addMarker: function() {
        var data = {};
        selectElement = this.refs.markerType.getDOMNode();
        var title = this.refs.title.getDOMNode().value.trim();
        if (selectElement.value == "S") {
            if (title) {
                data = {
                    'video': this.props.videoId,
                    'time': $(this.refs.slider.getDOMNode()).slider("value"),
                    'type': 'S',
                    'title': title,
                };
            } else {
                addErrorClassFn = function() {
                    $(this.refs.title.getDOMNode().parentNode).addClass("has-error");
                    console.log(this.refs.title.getDOMNode().parentNode);
                }.bind(this);
                this.updateMarkerResult({'error': true, 'msg': "Marker Title required"}, addErrorClassFn);
                return;
            }
            this.postMarkerData(data);
        } else {
            request = this.createQuiz(title)
            request.done(function(response) {
                response = jQuery.parseJSON(response);
                data = {
                    'video': this.props.videoId,
                    'time': $(this.refs.slider.getDOMNode()).slider("value"),
                    'type': 'Q',
                    'quiz': response['id']
                };
                this.postMarkerData(data);
            }.bind(this));
        }
    },

    componentDidUpdate: function() {
        initial_time = 0;
        if (this.props.marker) {
            initial_time = this.props.marker.time;
        }
        $(this.refs.slider.getDOMNode()).slider("value", initial_time);

        this.loadQuiz();
    },

    componentWillReceiveProps: function(nextProps) {
        this.setState({
            videoLength: nextProps.videoLength,
            error_messages: [], quizLoaded: false
        });
    },

    loadQuiz: function() {
        // Load the quiz if the marker is a quiz marker
        marker = this.props.marker;
        if (marker && marker['type'] != 'S' && !this.state.quizLoaded){
            var url = "/quiz/api/quiz/" + marker.quiz + "/?format=json";
            request = ajax_json_request(url, "GET", {});
            request.done(function(response) {
                response = jQuery.parseJSON(response);
                this.setState({quiz: response, quizLoaded: true});
            }.bind(this));
        }
    },

    componentDidMount: function() {
        this.loadQuiz();

        // Initialising the slider to get video time for marker
        initial_time = 0;
        if (this.props.marker) {
            initial_time = this.props.marker.time;
        }

        toTime = function(t) {
            sec = t%60;
            min = (t-sec)/60;
            if (sec < 10) {
                sec = "0"+sec;
            }
            if (min < 10) {
                min = "0"+min;
            }
            return min + ":" + sec;
        };

        sliderToolTipCreate = function(event, ui) {
            var curValue = ui.value || $(this.refs.slider.getDOMNode()).slider("value");
            var tooltip = '<div class="slider-tooltip"><div class="slider-tooltip-inner">' + toTime(curValue) +
                          '</div><div class="slider-tooltip-arrow"></div></div>';
            $('.ui-slider-handle').html(tooltip);
        }.bind(this);

        sliderToolTip = function(event, ui) {
            var curValue = ui.value || $(this.refs.slider.getDOMNode()).slider("value");
            var tooltip = '<div class="slider-tooltip"><div class="slider-tooltip-inner">' + toTime(curValue) +
                          '</div><div class="slider-tooltip-arrow"></div></div>';
            $('.ui-slider-handle').html(tooltip);
        }.bind(this);

        $(this.refs.slider.getDOMNode()).slider({
            min: 0,
            max: Math.floor(this.state.videoLength),
            value: initial_time,
            step: 1,
            slide: sliderToolTip,
            create: sliderToolTipCreate,
            change: sliderToolTip,
        });
        console.log(this.refs.slider.getDOMNode());

    },

    showMarkerSection: function() {
        selectElement = this.refs.markerType.getDOMNode();
        if (selectElement.value == "S") {
            //$(this.refs.addQuizMarker.getDOMNode())[0].style["display"]="none";
            //$(this.refs.addSectionMarker.getDOMNode())[0].style["display"]="inline-block";
        } else {
            //$(this.refs.addSectionMarker.getDOMNode())[0].style["display"]="none";
            //$(this.refs.addQuizMarker.getDOMNode())[0].style["display"]="inline-block";
        }
    },

    getInitialState: function() {
        return {
            videoLength: this.props.videoLength,
            error_messages: [],
            quizLoaded: false,
            quiz: undefined
        }
    },


    render: function() {
        form = null;
        error_messages = this.state.error_messages.map( function(error, index) {
            return <li class="form-error-msg" key={"form-error-msg-" + index}> {error} </li>;
        });
        error_div = undefined;
        if (error_messages.length > 0) {
            error_div = <div class="row">
                            <div class="col-md-6 col-md-offset-3">
                                <ul class="form-error alert alert-danger">
                                    {error_messages}
                                </ul>
                            </div>
                        </div>;
        }
        if (! this.props.marker) {
            // Add new Marker Form
            form = <form id='add-marker' role="form">
                        <span class="text-center marker-form-heading">
                            <button type="button" onClick={this.cancelAddMarker}
                                class="btn btn-danger pull-left"> Cancel </button>
                            Add Marker
                            <button type="button" onClick={this.addMarker}
                                class="btn btn-success pull-right"> Add </button>
                        </span>
                        <div>
                            <div ref="slider" id="slider"/>
                        </div>
                        {error_div}
                        <div class="form-marker-content">
                                <select ref="markerType" onChange={this.showMarkerSection} class="marker-type">
                                    <option name="marker_type" type="text" value="S"> Section Marker </option>
                                    <option name="marker_type" type="text" value="Q"> Quiz Marker </option>
                                </select>
                                <span ref="addSectionMarker" id="addSectionMarker" class="form-marker-title-span">
                                    <input name="title" type="text" ref="title" class="form-control form-marker-title"
                                            placeholder="Marker Title"/>
                                </span>
                        </div>
                    </form>;
        } else {
            marker = this.props.marker;
            if (marker['type'] == 'S') {
                // Update Section Marker
                form = <form id='update-section-marker' role="form">
                            <span class="text-center marker-form-heading">
                                <button type="button" onClick={this.deleteMarker}
                                    class="btn btn-danger pull-left"> Delete </button>
                                Update Section Marker
                                <button type="button" onClick={this.updateSectionMarker}
                                    class="btn btn-success pull-right"> Update </button>
                            </span>
                            <div>
                                <div ref="slider" id="slider"/>
                            </div>
                            {error_div}
                            <div class="form-marker-content">
                                <input name="title" type="text" ref="title" class="form-control"
                                    placeholder="Marker Title" defaultValue={marker.title} />
                            </div>
                        </form>;
            } else if (marker['type'] == 'Q') {
                // Update Quiz Marker
                // TODO(Aakash Rao) : Add the panel for In Video Quiz Module
                form = <form id='update-section-marker' role="form">
                            <span class="text-center marker-form-heading">
                                <button type="button" onClick={this.deleteMarker}
                                    class="btn btn-danger pull-left"> Delete </button>
                                Update Quiz Marker
                                <button type="button" onClick={this.updateQuizMarker}
                                    class="btn btn-success pull-right"> Update </button>
                            </span>
                            <div>
                                <div ref="slider" id="slider"/>
                            </div>
                            <div class="form-marker-content">
                                {this.state.quizLoaded ?
                                    <div>
                                        <input name="title" type="text" ref="title" class="form-control"
                                            placeholder="Marker Title" defaultValue={this.state.quiz.title} />
                                        <div>
                                            <QuizEditAdmin quiz={this.state.quiz} />
                                            <div id={QuestionModuleEditId} />
                                        </div>
                                    </div> :
                                    <LoadingBar />
                                }
                            </div>
                        </form>;
            }
        }
        return (
            <div class="row marker-area" id="marker-area">
                {form}
            </div>
        );
    }
});
