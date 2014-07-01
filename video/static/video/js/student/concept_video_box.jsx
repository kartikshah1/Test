/** @jsx React.DOM */


/**
    Concept Video Box for Student.
    This will be rendered in student_concept.jsx
    Provides features to :-
        1.  Upvote
        2.  DownVote
**/


/**
    ConceptVideoBox [R]
        -   Video Navigation
        -   VideoTOC [R]
        -   VideoVote [R]
        -   Video [R]
**/

var ConceptVideoBox = React.createClass({
    mixins: [ScrollToElementMixin],

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

    updateVote: function(newVotes, newVote) {
        if (newVote == this.state.vote) {
            newVote = 'N';
        }
        this.setState({
            votes: newVotes,
            vote: newVote,
        });
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
            votes: [data.content.upvotes, data.content.downvotes],
            vote: data.history.vote,
            startTime: 0,
        };
    },

    render: function() {
        data = this.props.data;
        marker = undefined;
        if (this.current_marker != -1) {
            marker = this.state.markers[this.state.current_marker];
        } else {
            marker = undefined;
        }
        return (
            <div class="row" class="concept-video-box">
                <div class="col-md-4 panel-group video-sidebar" id="video-sidebar">
                    <VideoContent content={this.state.content} title={this.state.title} />
                    <VideoTOC markers={this.state.markers} clickCallback={this.changeCurrent} />
                    {this.props.data.content.other_file != '/media/' ?
                        <VideoSlide other_file={this.props.data.content.other_file} />
                        : null
                    }
                </div>
                <div class="col-md-8 video-container" id="video-container">
                    <VideoNavigation
                        nextVideo={this.props.nextCallback}
                        prevVideo={this.props.prevCallback}
                        title={this.state.title} />
                    <Video videoFile={data.content.video_file} videoStartTime={this.state.startTime}
                        markers={this.state.markers} />
                    <VideoVote votes={this.state.votes} updateVote={this.updateVote}
                        vote={this.state.vote} videoId={data.content.id}/>
                </div>
            </div>
        );
    }
});


/**
    VideoSlide
        -   slide link
**/
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
                                <a href={this.props.other_file} target="_blank">Slides</a>
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

    render: function() {
        console.log("props of the video are : ");
        console.log(this.props);
        return (
            <div class="panel panel-default video-desc-container" id="content-container" ref="videoContentDiv">
                <div class="panel-heading" data-toggle="collapse"
                    data-parent="#video-sidebar" data-target="#video-description">
                    <span class="video-sidebar-heading"> Description </span>
                </div>
                <div class="video-sidebar-content panel-collapse collapse in" id="video-description">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="video-desc">
                                <h4> {this.props.title} </h4>
                                <p> {this.props.content} </p>
                            </div>
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
        console.log(this.props.markers);
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
        var toc = <div />;
        if (markers.length != 0) {
            toc = <div class="panel panel-default video-toc-container" id="toc-container">
                        <div class="panel-heading" data-toggle="collapse" data-parent="#video-sidebar"
                            data-target="#toc">
                            <span class="video-sidebar-heading"> Table of Content </span>
                        </div>
                        <div class="video-sidebar-content panel-collapse collapse" id="toc">
                            <ul id="tocList" role="menu" class="tocList">
                                {markers}
                            </ul>
                        </div>
                    </div>;
        }
        return (toc);
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

    seen_markers: [],

    video: undefined,

    componentWillReceiveProps: function(nextProps) {
        all_markers = nextProps.markers;
        quiz_markers = [];
        this.seen_markers = [];
        for (var i = 0; i < all_markers.length; i++) {
            if (all_markers[i]['type'] == 'Q') {
                quiz_markers.push({
                    id: all_markers[i].id,
                    time: all_markers[i].time,
                    quiz: all_markers[i].quiz
                });
                this.seen_markers.push(false);
            }
        }
        this.setState({quiz_markers: quiz_markers});
        videoStartTime = nextProps.videoStartTime;
        _V_("video-player").ready(function() {
            setTimeout(function(){
                video.currentTime = videoStartTime;
                console.log("Return from video set time");
            }, 1);
        });
    },

    componentDidUpdate: function() {
        this.video = document.getElementsByTagName("video")[0];
        video = this.video;
        //console.log("Return from video did update");
    },

    inEpsilon: function(value, list, delta) {
        //console.log("Searching index");
        //seen_markers = this.state.seen_markers;
        for (var i = 0; i < list.length; i++) {
            if (this.seen_markers[i] == false && value > list[i] - delta && value < list[i] + delta) {
                return i;
            }
        }
        return -1;
    },

    openDiv: function(index, video) {
        //console.log("Opening div for " + index);
        video.pause();
        player = VideoJS("video-player", {}, function(){ console.log("Player set for exit fullscreen");});
//        console.log("Trying to exit Full Screen");
//        console.log(player.isFullScreen);
        if (player && player.isFullScreen) {
            alert("Please exit FullScreen and attempt Quiz.");
//            console.log(player);
//            var e = CustomEvent("keypress");
//            e.keyCode = 13; e.which = 13;
//            document.dispatchEvent(e);
//            if (confirm("Please exit fullscreen and attempt Quiz")) {
//                player.cancelFullScreen();
//                document.mozCancelFullScreen();
//                video.mozCancelFullScreen();
//            }
        }
        //seen_markers = this.state.seen_markers;
        this.seen_markers[index] = true;
        //this.setState({seen_markers: seen_markers});
        //console.log(this.state.quiz_markers[index]);
        this.setState({current_quiz: this.state.quiz_markers[index].quiz});
    },

    componentDidMount: function() {
        this.video = document.getElementsByTagName("video")[0];
        this.video.oncontextmenu = function() { return false; };
        video = this.video;
        inEpsilon = this.inEpsilon;
        openDiv = this.openDiv;
        quiz_markers = this.state.quiz_markers;
        _V_("video-player").ready(function() {
            setTimeout(function(){
                console.log(quiz_markers);
                all_time = quiz_markers.map(function(q_m) {return q_m.time;});
                console.log(all_time);
                video.addEventListener("timeupdate", function() {
                    //console.log(video.currentTime);
                    index = inEpsilon(video.currentTime, all_time, 0.25);
                    if (index >= 0){
                        openDiv(index, video);
                    }
                    //console.log(video.currentTime);
                }.bind(video, inEpsilon, all_time, openDiv));
               /* document.addEventListener("keypress", function(e) {
//                    console.log(e);
                    var code = (e.keyCode ? e.keyCode : e.charCode)
//                    console.log(code);
                    if (code == 32) {
                        if (video.paused) {
                            video.play();
                        } else {
                            video.pause();
                        }
                    }  else if (code == 27) {
                        console.log("Event to exit FullScreen");
                        if (document.mozCancelFullScreen) {
                            document.mozCancelFullScreen();
                            video.mozCancelFullScreen();
                        } else {
                            document.webkitCancelFullScreen();
                            video.mozCancelFullScreen();
                        }
                    }
                });*/
            }, 1);
        });
    },

    getInitialState: function() {
        all_markers = this.props.markers;
        quiz_markers = [];
        this.seen_markers = [];
        for (var i = 0; i < all_markers.length; i++) {
            if (all_markers[i]['type'] == 'Q') {
                quiz_markers.push({
                    id: all_markers[i].id,
                    time: all_markers[i].time,
                    quiz: all_markers[i].quiz
                });
                this.seen_markers.push(false);
            }
        }
        return {
            quiz_markers: quiz_markers,
            current_quiz: undefined
        };//, seen_markers: seen_markers};
    },

    unsetCurrentQuiz: function(play){
        this.setState({current_quiz : undefined});
        if(play) this.video.play();
    },

    render: function() {
        file = this.props.videoFile;
        return (
            <div>
                <div class="video">
                    <video ref="videoPlayer" id="video-player" class="video-js vjs-default-skin"
                        controls autobuffer preload="auto" width="720" height="480" data-setup='{}'>
                        <source type='video/webm' src={file} />
                        <source type='video/mp4' src={file} />
                        <track src="/media/static/video/a.srt" srclang="en" label="English" default />
                    </video>
                </div>
                {this.state.current_quiz != undefined ?
                    <ConceptQuiz id={this.state.current_quiz}
                        closeCallback={this.unsetCurrentQuiz.bind(this,true)} />
                    : null
                }
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

    base_url: "/video/api/",

    sendVote: function(data, method) {
        url = this.base_url + "video/" + this.props.videoId + "/vote/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            console.log(response);
            response = jQuery.parseJSON(response);
            if (method == this.state.vote) {
                method = 'N'
            }
            this.setState({
                vote: method,
                upvotes: response['vote'][0],
                downvotes: response['vote'][1],
            });
            //this.props.updateVote(response['vote'], method);
        }.bind(this));
    },

    upvote: function() {
        data = {'vote': 'up'};
        this.sendVote(data, 'U');
    },

    downvote: function() {
        data = {'vote': 'down'};
        this.sendVote(data, 'D');
    },

    componentWillReceiveProps: function(nextProps) {
        console.log(nextProps);
        this.setState({
            vote: nextProps.vote,
            upvotes: nextProps.votes[0],
            downvotes: nextProps.votes[1]
        });
    },

    getInitialState: function() {
        return {
            vote: this.props.vote,
            upvotes: this.props.votes[0],
            downvotes: this.props.votes[1]
        };
    },

    render: function() {
        if (this.state.vote == 'U') {
            Upvote = <b> Upvote </b>;
        } else {
            Upvote = "Upvote";
        }
        if (this.state.vote == 'D') {
            Downvote = <b> Downvote </b>;
        } else {
            Downvote = "Downvote";
        }
        return (
            <div class="row video-vote">
                <span class="pull-right">
                    <span class="vote">
                        <span class="text-success" onClick={this.upvote}>
                            {Upvote} </span> : {this.state.upvotes}
                    </span>
                    <span class="vote">
                        <span class="text-danger" onClick={this.downvote}>
                            {Downvote} </span> : {this.state.downvotes}
                    </span>
                </span>
            </div>
        );
    }
});
