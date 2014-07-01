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
            content = <CourseStudent courseid={this.props.courseid} />
        }
        else if(this.props.id=="-7") {
            content = <AddPageForm heading="Add Page" saveCallBack={this.props.callback} />;
        }
        else if (this.props.id=="-8") {
            content = <CourseSettings courseid={this.props.courseid} />;
        }
        else if(this.props.id > 0) {
            content = <Page id={this.props.id} deleteCallBack={this.props.deleteCallBack}/>;
        }
        else {
            content = <LoadingBar />;
        }
        return (
            <div>{content}</div>
        );
    }
});

var CourseBody = React.createClass({
    mixins: [SortableMixin],
    getInitialState: function() {
        return {
            loaded: false,
            pages: undefined,
            id: this.props.page_ref,
            order: false
        };
    },

    addPage: function(data) {
        url = "/courseware/api/course/" + this.props.id + "/add_page/?format=json";
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState['pages'].push(response);
            oldState['id']=response.id;
            this.setState(oldState);
        }.bind(this));
    },

    saveOrder: function(data) {
        url = "/courseware/api/course/" + this.props.id + "/reorder_pages/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            display_global_message("Successfully reordered the pages", "success");
            this.saveOrderSuccess("#sideList");
        }.bind(this));
    },

    handleDeletePage: function(pageid) {
        oldState = this.state;
        oldState['id']="-1";
        $("#page_"+pageid).remove();
        //v = parseInt(pageid);
        //newpages = this.state.pages.filter(function (page) {
        //    return (parseInt(page.id) != v);
        //});
        //oldState['pages'] = newpages;
        this.setState(oldState);
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
    
    getAssignmentLink: function(){
        return "/assignments/" + this.props.id;//state['id'];
    },

    componentDidUpdate: function() {
        if(!this.state.loaded) {
            this.loadPages();
        }
        else {
            $("#sideList li.selectedLink").removeClass("selectedLink");
            $("#sideList [value="+this.state.id+"]").addClass("selectedLink");
            if(this.state.order)
            {
                $(".page").addClass("sortable-items");
            }
            else {
                $(".page").removeClass("sortable-items");
            }
        }
    },

    myhandleSortClick: function() {
        this.handleSortClick("#sideList","li.page");
    },

    myhandleSaveOrder: function() {
        this.handleSaveOrder("#sideList",5);
    },

    render: function() {
        var pages = '';
        var page_order = '';
        if(this.state.loaded) {
            var pages = this.state.pages.map(
                function (page) {
                    return <li key={"p_"+page.id} id={"page_"+page.id} onClick={this.handleClick.bind(this, page.id)} class="page" value={page.id}>{page.title}</li>;
                }.bind(this));
            if (pages.length > 0) {
                if (!this.state.order) {
                    page_order = (
                        <li id="pageReorder" class="pagesort-btn"onClick={this.myhandleSortClick}>
                        <span class="glyphicon glyphicon-sort"></span>&nbsp;&nbsp;Reorder Pages
                        </li>
                    );
                }
                else {
                    page_order = (
                        <li id="pageOrderSave" class="pagesort-btn" onClick={this.myhandleSaveOrder}>
                            <span class="glyphicon glyphicon-save"></span>&nbsp;&nbsp;Save Current Order
                        </li>
                    );
                }
            }
        }
        return (
            <div>
                <div class="col-md-3 courseSidebar">
                    <ul id="sideList" class="courseLinks" role="menu" aria-labelledby="dLabel">
                        <li onClick={this.handleClick.bind(this, "-1")} value='-1'>Content</li>
                        <li onClick={this.handleClick.bind(this, "-2")} value='-2'>Information</li>
                        <li onClick={this.handleClick.bind(this, "-3")} value='-3'>Discussion</li>
                        <li onClick={this.handleClick.bind(this, "-5")} value='-5'>Progress</li>
                        <li onClick={this.handleClick.bind(this, "-6")} value='-6'>Students</li>
                        <li onClick={this.handleClick.bind(this, "-8")} value='-8'>Settings</li>
                        <li><a id="assignmentLink" href={this.getAssignmentLink()}>Assignments</a></li>
                        {page_order}
                        {pages}
                        <li class='addPageButton' onClick={this.handleClick.bind(this, "-7")} value='-7'>
                            Add Page
                            <span class='glyphicon glyphicon-plus-sign pull-right'> </span>
                        </li>
                    </ul>
                </div>
                <div class="col-md-9 courseBody">
                    <CourseContent id={this.state.id} courseid={this.props.id}
                        forumid={this.props.forumid} callback={this.addPage}
                        deleteCallBack={this.handleDeletePage}/>
                </div>
            </div>
        );
    }
});
