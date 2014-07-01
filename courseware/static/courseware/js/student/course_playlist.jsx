/** @jsx React.DOM */

var ConceptPlaylist = React.createClass({
    render: function() {
        itemNodes = this.props.list.map(function(item, i) {
            return (
                <li key={i}>
                    <ConceptPlaylistItem
                        index={i}
                        type={item.type}
                        title={item.title} id={item.id}
                        content = {item}/>
                </li>
            );
        }.bind(this));
        return (
            <div>
                <ul class="list-inline concept-playlist">
                    {itemNodes}
                </ul>
            </div>
        );
    }
});

var ConceptPlaylistItem = React.createClass({

    getLink: function() {
        link = '';
        if (this.props.content.type=="document"){
            content = this.props.content.content;
            documents = content.sections.map(function(item, i) {
            if (!item.file){
                return(
                    ''
                );
            } else {
                return(
                    <li key={i}>
                        <a href={item.file}  data-container="body" data-toggle="popover"
                        data-trigger="hover" data-placement="bottom" title="" data-original-title=""
                     ref="linkBlock" target="_blank">
                    <span class={"glyphicon glyphicon-file"}></span></a>
                    </li>
                );
            }
        });
        return (
            <div>
            <ul class="list-unstyled concept-document-sections">
                    {documents}
                </ul>
            </div>
        );
    }

    else if (this.props.content.type=="video"){
        content = this.props.content;
        if(content.content.other_file!='/media'){
            return (
                    <a href={content.content.other_file}  data-container="body" data-toggle="popover"
                    data-trigger="hover" data-placement="bottom" title="" data-original-title=""
                    ref="linkBlock" target="_blank">
                    <span class={"glyphicon glyphicon-credit-card"}></span></a>
                                           );
        }
        else{
            return ('');
        }

    }
    else{
        return ('');
    }
    },
    render: function() {
        isVideo = this.props.type == "video";
        isQuiz = this.props.type == "quiz";
        return (
            <div class="concept-playlist-item">
            {this.getLink()}
            </div>
        );
    }
});



var Concept = React.createClass({
    base_url: "/concept/api/",
    getInitialState: function() {
        return {
            loaded: false,
            data: undefined,
            highlight: undefined,
        };
    },
    loadData: function() {
        url = this.base_url + "concept/" + this.props.concept.id + "/get_concept_page_data";
        $.ajax({
            url: url,
            dataType: 'json',
            mimeType: 'application/json',
            data: {format: 'json'},
            success: function(data) {
                state = this.state;
                state.loaded = true;
                state.data = data
                this.setState(state);
            }.bind(this)
        });
    },

    componentDidMount: function() {
        if (!this.state.loaded) this.loadData();
    },

    render: function() {

        if (!this.state.loaded){
            return (
                <div>
                    <LoadingBar />
                </div>
            );
        }
        else
            {
                links = '';
                /*data = this.state.data.playlist.map(function(content){
                    type = content.type;
                    isVideo = type == "video";
                    isDocument = type == "document";
                    isQuiz = type == "quiz";
                  return  (<a href={"" + (isVideo ? content.content.video_file: content.content.sections[0].file)} data-container="body" data-toggle="popover"
                    data-trigger="hover" data-placement="bottom"
                    title="" data-original-title=""
                     ref="linkBlock">
                    <span class={"glyphicon glyphicon-" +
                        (isVideo ? "film" : ( isQuiz ? "question-sign" : "file"))}></span>
            </a>);

                });*/

                return (
                    <li class='concept'>
                        <a href={'/concept/' + this.props.concept.id + '/'} class="concept-title">
                            {this.props.concept.title}
                        </a>
                        <div class="pull-right">
                            <div class="panel-footer">
                                <ConceptPlaylist
                                    conceptId={this.props.concept.id}
                                    list={this.state.data.playlist}
                                    />
                            </div>
                        </div>
                    </li>
                );
    }       }
});

var Group = React.createClass({

    getInitialState: function() {
        return {
            loaded: false,
            concepts: undefined,
            title: this.props.group.title,
            description: this.props.group.description,
        };
    },

    loadConcepts: function() {
        url = "/courseware/api/group/" + this.props.group.id + "/published_concepts/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState['concepts'] = response;
            oldState['loaded'] = true;
            this.setState(oldState);
        }.bind(this));
    },

    componentDidMount: function() {
        if(!this.state.loaded) {
            this.loadConcepts();
        }
    },

    componentDidUpdate: function() {
        if(!this.state.loaded) {
            this.loadConcepts();
        }
    },

    render: function() {
        if(!this.state.loaded) {
            content = <LoadingBar />;
        }
        else {
            var concepts = this.state.concepts.map(function (concept) {
                    return <Concept concept={concept} />;
                }.bind(this));
            var groupid = 'group_' + this.props.group.id;
            content = (
                <div class="panel panel-default group">
                    <div class="panel-heading" data-toggle="collapse" data-parent="#accordion" data-target={"#"+groupid}>
                        <div class="panel-title group-heading">
                            {this.state.title}
                        </div>
                        <div class="muted">
                            <span dangerouslySetInnerHTML={{__html: converter.makeHtml(this.state.description)}} />
                        </div>
                    </div>
                    <div id={groupid} class="panel-collapse collapse">
                        <div class="panel-body group-inner">
                            <ul class="concepts">
                                {concepts}
                            </ul>
                        </div>
                    </div>
                </div>
            );
        }
        return content;
    }
});

var CoursePlaylist = React.createClass({

    loadGroups: function() {
        url = "/courseware/api/course/" + this.props.courseid + "/groups/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState['groups'] = response;
            oldState['loaded'] = true;
            this.setState(oldState);
        }.bind(this));
    },

    getInitialState: function() {
        return {
            loaded: false,
            groups: undefined,
        };
    },

    componentDidMount: function() {
        if(!this.state.loaded) {
            this.loadGroups();
        }
    },

    componentDidUpdate: function() {
        if(this.state.loaded) {
            $("#groups").accordion({
                animate: 100,
                collapsible: true,
                heightStyle: "content"
            });
            //$("#groups li").disableSelection();
        }
        else {
            this.loadGroups();
        }
    },

    render: function() {
        if(!this.state.loaded) {
            groups = <LoadingBar />;
        }
        else {
            if (this.state.groups == "")
                groups = (<div class="alert alert-danger alert-dismissable">No content displayed yet in this course</div>);
            else {
                var i = 0;
                groups = this.state.groups.map(
                function (group) {
                    i = i+1;
                    return <Group group={group}/>;
                }.bind(this));
            }
        }
        return (
            <div>
                <h3 class='contentheading'>
                    Course Content
                </h3>
                <div class="panel-group" id="accordion">
                    {groups}
                </div>
            </div>
        );
    }
});
