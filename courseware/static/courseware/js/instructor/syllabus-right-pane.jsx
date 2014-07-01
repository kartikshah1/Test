/** @jsx React.DOM */

var MY_GLOBAL_VARS = {
    groupid: 0,
    conceptid: 0,
    elementid:0
}

var SyllabusConcept = React.createClass({
    mixins: [LoadMixin],

    getUrl: function() {
        return '/courseware/api/concept/' + this.props.concept.id + '/playlist/?format=json';
    },

    render: function() {
        var content = '';
        if (this.state.loaded)
        {
            number=0;
            content = this.state.data.map(function (object) {
                    number += 1;
                    return <div key={number}><a>Video: {object.title}</a></div>;
                }.bind(this));
        }
        return (
            <div id={'syllabus-concept-tobecopied-'+this.props.keyid} value={this.props.concept.id}  data-myvar={this.props.mykey} class='panel panel-default panel-search-area syllabus-concept-in-sortable'>
                <div class='panel-heading concept-syllabus-handle' data-toggle='collapse' data-target={'#syllabus-concept-' + this.props.keyid}>
                    Concept: {this.props.concept.title}
                </div>
                <div id={'syllabus-concept-'+this.props.keyid} class='syllabus-concept-collapse-box panel-collapse collapse'>
                    {content}
                </div>
            </div>
        );
    }
});



var SyllabusGroup = React.createClass({
    mixins: [LoadMixin],

    getUrl: function() {
        return '/courseware/api/group/' + this.props.group.id + '/concepts/?format=json';
    },

    getInitialState: function() {
        return {
            clientloaded: true
        };
    },

    componentDidUpdate: function() {
        $('#concepts-syllabus-area-'+this.props.keyid).droppable({
            activeClass: "syllabus-right-pane-activate",
            hoverClass: "syllabus-right-pane-hover",
            accept: ".search-concept",
            drop: function(event, ui) {
                MY_GLOBAL_VARS.conceptid = MY_GLOBAL_VARS.conceptid + 1;
                keyid = 'n' + MY_GLOBAL_VARS.conceptid;
                myid = $(ui.draggable)[0].id.substring(26);
                mydata = this.state.data;
                mydata.push({'keyid': keyid, id: myid, 'title':$(ui.draggable).find('.panel-heading')[0].innerText.substring(9)});
                //console.log(this.props.group.id+" drop " + myid);
                this.setState({data: mydata, clientloaded: true});
            }.bind(this)
        }).sortable({
            cursor: "move",
            axis: "y",
            handle: '.concept-syllabus-handle',
            items: ".syllabus-concept-in-sortable",
            connectWith: ".syllabus-concepts",
            placeholder: "state-highlight",
            forcePlaceholderSize: true,
            start: function(event, ui) {
                $(ui.item).addClass("being-dragged");
                $(this).data('startindex', ui.item.index());
                $(this).data('inside', true);
            }.bind(this),
            beforeStop: function(event, ui) {
            },
            stop: function(event, ui) {
                //console.log(this.props.group.id);
                $(ui.item).removeClass("being-dragged");
                var inside = $(this).data('inside');
                if(inside) {
                    startindex = parseInt($(this).data('startindex'));
                    endindex = parseInt(ui.item.index());
                    //console.log(startindex);
                    //console.log(endindex);
                    $('#concepts-syllabus-area-'+this.props.keyid).sortable("cancel");
                    concepts = this.state.data;
                    temp = concepts[startindex];
                    concepts.splice(startindex, 1);
                    concepts.splice(endindex, 0, temp);
                    //console.log(concepts);
                    this.setState({data: concepts});
                    //$('#concepts-syllabus-area-'+this.props.group.id).sortable("cancel");
                }
                else {
                    //event.preventDefault();
                    //v = $(ui.item)[0].getAttribute('value');
                    //$('#concepts-syllabus-area-'+this.props.group.id).sortable("cancel");
                    //ui.item.remove();
                    startindex = parseInt($(this).data('startindex'));
                    concepts = this.state.data;
                    concepts.splice(startindex, 1);
                    loaded = !(concepts.length == 0);
                    //console.log(this.props.group.id+"remove" + v);
                    //console.log(newconcepts);
                    //setTimeout(function() {
                        this.setState({data: concepts, clientloaded: loaded});
                    //}.bind(this), 200);
                }
                //$(ui.item).remove();
            }.bind(this),
            receive: function(event, ui) {
                endindex = ui.item.index();
                $(ui.sender).sortable("cancel");
                //$('#concepts-syllabus-area-'+this.props.group.id).sortable("cancel");
                //event.preventDefault();
                //ui.item.remove();
                //$(ui.item).addClass('extra-garbage');
                //setTimeout(function() {
                //    $('.extra-garbage').remove();
                //    console.log($(".extra-garbage"));
                //}, 100);
                //setTimeout(function() {
                    myid = $(ui.item)[0].getAttribute('value');
                    keyid = $(ui.item)[0].getAttribute('data-myvar');
                    console.log(keyid);
                    //console.log(myid);
                    mydata = this.state.data;
                    mydata.splice(endindex, 0, {'keyid': keyid, 'id':myid, 'title':$(ui.item).find('.panel-heading')[0].innerText.substring(9)});
                    //console.log(this.props.group.id+" sortable receive " + myid);
                    this.setState({data: mydata, clientloaded: true});
                //}.bind(this), 100);
            }.bind(this),
            remove: function(event, ui) {
                $(this).data('inside', false);
            }.bind(this)
        });
    },

    handleDelete: function() {
        if(this.props.keyid[0]!='n') {
            url = "/courseware/api/group/" + this.props.group.id + "/?format=json";
            request = ajax_json_request(url, "DELETE",{});
            request.done(function(response) {
                display_global_message("Successfully deleted the group", "success");
                this.props.callback(this.props.keyid);
            }.bind(this));
        }
        else {
            this.props.callback(this.props.keyid);
        }
        return false;
    },

    handleEdit: function(data) {
        url = "/courseware/api/group/" + this.props.group.id + "/?format=json";
        request = ajax_json_request(url, "PATCH", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            display_global_message("Successfully updated the group", "success");
            oldState = this.state;
            oldState['title'] = response.title;
            oldState['description'] = response.description;
            oldState['showform'] = false;
            this.setState(oldState);
        }.bind(this));
    },

    render: function() {
       // console.log("I am "+ this.props.group.id);
        var content = (
            <div class='panel panel-default panel-search-area'>
                <div class='panel-heading'>
                    No content till now.
                </div>
            </div>
        );
        if (this.state.loaded && this.state.clientloaded && this.state.data.length > 0)
        {
            content = this.state.data.map(function (object) {
                //do something to differentiate the key of 2 copies of the same copncept dragged into this
                if(object.keyid) {
                    keyid = object.keyid;
                }
                else {
                    keyid = object.id;
                }
                return <SyllabusConcept key={this.props.keyid+'_'+keyid} mykey={keyid} keyid={this.props.keyid+'_'+keyid} concept={object}/>;
            }.bind(this));
        }
        return (
            <div class='panel panel-default panel-search-area'>
                <div class='panel-heading group-syllabus-handle' data-toggle='collapse' data-target={'#syllabus-group-' + this.props.keyid}>
                    Group: {this.props.group.title}
                    <validateDeleteBtn label={"syllabusgroup_"+this.props.group.id+"Label"} modal={"syllabusgroup_"+this.props.group.id+"Modal"} callback={this.handleDelete} heading="group" />
                    <div class="pull-right">
                        <span class="glyphicon glyphicon-save"></span>
                        <span class="glyphicon glyphicon-edit"></span>
                        <a data-toggle="modal" href={"#syllabusgroup_"+this.props.group.id+"Modal"}>
                            <span class="glyphicon glyphicon-trash"></span>
                        </a>
                    </div>
                </div>
                <div id={'syllabus-group-'+this.props.keyid} class='syllabus-group-collapse-box panel-collapse collapse'>
                    <div class='panel-group syllabus-concepts' id={'concepts-syllabus-area-'+this.props.keyid}>
                        {content}
                    </div>
                </div>
            </div>
        );
    }
});


var SyllabusGroups = React.createClass({
    mixins: [LoadMixin, SavedStatusMixin, BackgroundTransitionMixin],

    getUrl: function() {
        return '/courseware/api/course/' + this.props.id + '/groups/?format=json';
    },

    componentDidUpdate: function() {
        $('#groups-syllabus-area').droppable({
            activeClass: "syllabus-right-pane-activate",
            hoverClass: "syllabus-right-pane-hover",
            accept: ".search-group",
            drop: function(event, ui) {
               // console.log('fasfasd');
                MY_GLOBAL_VARS.groupid = MY_GLOBAL_VARS.groupid + 1;
              //  console.log('fasfasd');
                keyid = 'n' + MY_GLOBAL_VARS.groupid;
                myid = $(ui.draggable)[0].id.substring(24);
                mydata = this.state.data;
                mydata.push({'keyid': keyid, 'id':myid, 'title':$(ui.draggable).find('.panel-heading')[0].innerText.substring(7)});
                //console.log(" drop " + myid);
                //console.log(" drop " + keyid);
                this.setState({data: mydata});
            }.bind(this)
        }).sortable({
            cursor: "move",
            axis: "y",
            handle: ".group-syllabus-handle",
            placeholder: "state-highlight",
            forcePlaceholderSize: true,
            start: function(event, ui) {
                $(ui.item).addClass("being-dragged");
            },
            stop: function(event, ui) {
                $(ui.item).removeClass("being-dragged");
            },
            receive: function(event, ui) {
                //console.log("sortable");
            }
        });
    },

    handleDelete: function(id) {
        data = this.state.data;
        newdata = data.filter(function (group) {
            if (group.keyid) {
                return (group.keyid != id);
            }
            else {
                return (parseInt(group.id) != parseInt(id));
            }
        });
        this.setState({data: newdata});
    },

    render: function() {
        var content = '';
        if (this.state.loaded)
        {
            content = this.state.data.map(function (object) {
                if(object.keyid) {
                    keyid = object.keyid;
                }
                else {
                    keyid = object.id;
                }
                return <SyllabusGroup key={keyid} keyid={keyid} group={object} callback={this.handleDelete}/>;
            }.bind(this));
        }
        return (
            <div class='panel-group syllabus-groups' id='groups-syllabus-area'>
                {content}
            </div>
        );
    }
});



/*
*/
var Syllabus = React.createClass({
    render: function() {
        return (
            <div>
            <h3>
                Syllabus
            </h3>
            <SyllabusGroups id={this.props.id}/>
            </div>
        );
    }
});