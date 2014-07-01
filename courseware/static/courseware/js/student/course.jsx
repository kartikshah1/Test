/** @jsx React.DOM */

var CourseContent = React.createClass({
    render: function() {
        var content = "";
        if(this.props.id=="-1") {
            content = <CoursePlaylist courseid={this.props.courseid}/>;
        }
        else if(this.props.id=="-2") {
            content = <CourseInfo course={this.props.courseid}/>;
        }
        else if(this.props.id=="-3") {
            content = <Forum id={this.props.forumid} />;
        }
        else if(this.props.id=="-5") {
            content = <Progress course={this.props.courseid}/>;
        }
        else if(this.props.id=="-6") {
            content = <PublicProgress course={this.props.courseid}/>;
        }
        else if(this.props.id > 0) {
            content = <Page id={this.props.id} />;
        }
        else {
            content = <LoadingBar />
        }
        return (
            <div>{content}</div>
        );
    }
});

var CourseBody = React.createClass({

    getInitialState: function() {
        return {
            loaded: false,
            pages: undefined,
            id: "-1",
        };
    },

    loadPages: function() {
        url = "/courseware/api/course/" + this.props.id + "/pages/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState['pages']=response;
            oldState['loaded']=true;
            this.setState(oldState);
        }.bind(this));
    },

    componentDidMount: function() {
        if(!this.state.loaded) {
            this.loadPages();
        }
    },

    handleClick: function(id) {
        oldState = this.state;
        oldState['id'] = id;
        $("#sideList li.selectedLink").removeClass("selectedLink");
        $("#sideList [value="+id+"]").addClass("selectedLink");
        this.setState(oldState);
    },

    componentDidUpdate: function() {
        if(!this.state.loaded) {
            this.loadPages();
        }
        else {
            $("#sideList li.selectedLink").removeClass("selectedLink");
            $("#sideList [value="+this.state.id+"]").addClass("selectedLink");
        }
    },

    getAssignmentLink: function(){
        return "/assignments/" + this.props.id;//state['id'];
    },

    render: function() {
        var pages = '';
        if(this.state.loaded) {
            var pages = this.state.pages.map(
                function (page) {
                    return <li id={"page_"+page.id} onClick={this.handleClick.bind(this, page.id)} class="page" value={page.id}>{page.title}</li>;
                }.bind(this));
        }
        return (
            <div>
                <div class="col-md-3 courseSidebar">
                    <ul id="sideList" class="courseLinks" role="menu" aria-labelledby="dLabel">
                        <li onClick={this.handleClick.bind(this, "-1")} value='-1'>Content</li>
                        <li onClick={this.handleClick.bind(this, "-2")} value='-2'>Information</li>
                        <li onClick={this.handleClick.bind(this, "-3")} value='-3'>Discussion</li>
                        <li onClick={this.handleClick.bind(this, "-5")} value='-5'>Progress</li>
                        <li onClick={this.handleClick.bind(this, "-6")} value='-6'>Score Card</li>
                        <li><a id="assignmentLink" href={this.getAssignmentLink()}>Assignments</a></li>
                        {pages}
                    </ul>
                </div>
                <div class="col-md-9 courseBody">
                    <CourseContent id={this.state.id} courseid={this.props.id} forumid={this.props.forumid} />
                </div>
            </div>
        );
    }
});
