/** @jsx React.DOM */


var SearchConcept = React.createClass({
    mixins: [LoadMixin],

    componentWillReceiveProps: function(nextProps) {
        state = this.state;
        state.loaded = false;
        state.data = undefined;
        this.setState(state, this.loadData);
    },

    getUrl: function() {
        return '/courseware/api/concept/' + this.props.concept.id + '/playlist/?format=json';
    },

    render: function() {
        var content = '';
        if (this.state.loaded)
        {
            content = this.state.data.map(function (object) {
                    return <a>Video: {object.title}</a>;
                }.bind(this));
        }
        return (
            <div id={'search-concept-tobecopied-'+this.props.concept.id} class='panel panel-default panel-search-area search-concept'>
                <div class='panel-heading concept-search-handle' data-toggle='collapse' data-target={'#search-concept-' + this.props.concept.id}>
                    Concept: {this.props.concept.title}
                </div>
                <div id={'search-concept-'+this.props.concept.id} class='panel-collapse collapse'>
                    {content}
                </div>
            </div>
        );
    }
});



var SearchGroup = React.createClass({
    mixins: [LoadMixin],

    componentWillReceiveProps: function(nextProps) {
        state = this.state;
        state.loaded = false;
        state.data = undefined;
        this.setState(state, this.loadData);
    },

    getUrl: function() {
        return '/courseware/api/group/' + this.props.group.id + '/concepts/?format=json';
    },

    componentDidUpdate: function() {
        $('.search-concept').draggable({
            cursor: "move",
            cursorAt: {left: 5},
            revert: "invalid",
            handle: ".concept-search-handle",
            zIndex: 100,
            helper: function() {
                return $("<div class='panel panel-default'><div class='panel-heading'>Concept.....Drag me to the right side</div></div>");
            },
        });
    },

    render: function() {
        var content = '';
        if (this.state.loaded)
        {
            content = this.state.data.map(function (object) {
                    return <SearchConcept key={object.id} concept={object}/>;
                }.bind(this));
        }
        return (
            <div id={'search-group-tobecopied-'+this.props.group.id} class='panel panel-default panel-search-area search-group'>
                <div class='panel-heading group-search-handle' data-toggle='collapse' data-target={'#search-group-' + this.props.group.id}>
                    Group: {this.props.group.title}
                </div>
                <div id={'search-group-'+this.props.group.id} class='panel-collapse collapse'>
                    <div class='panel-group' id={'concepts-search-area-'+this.props.group.id}>
                        {content}
                    </div>
                </div>
            </div>
        );
    }
});


var SearchGroups = React.createClass({
    mixins: [LoadMixin],

    componentWillReceiveProps: function(nextProps) {
        state = this.state;
        state.loaded = false;
        state.data = undefined;
        this.setState(state, this.loadData);
    },

    getUrl: function() {
        return '/courseware/api/course/' + this.props.id + '/groups/?format=json';
    },

    componentDidUpdate: function() {
        $('#groups-search-area .search-group').draggable({
            cursor: "move",
            cursorAt: {left: 5},
            revert: "invalid",
            handle: ".group-search-handle",
            zIndex: 100,
            helper: function() {
                return $("<div class='panel panel-default'><div class='panel-heading'>Group.....Drag me to the right side</div></div>");
            },
        });
    },

    render: function() {
        var content = '';
        if (this.state.loaded)
        {
            content = this.state.data.map(function (object) {
                    return <SearchGroup key={object.id} group={object}/>;
                }.bind(this));
        }
        return (
            <div class='panel-group' id='groups-search-area'>
                {content}
            </div>
        );
    }
});


var List = React.createClass({
    mixins: [LoadMixin],

    componentWillReceiveProps: function(nextProps) {
        state = this.state;
        state.loaded = false;
        state.data = undefined;
        this.setState(state, this.loadData);
    },

    getUrl: function() {
        return '/courseware/api/' + this.props.url + 'format=json';
    },

    handleClick: function (event) {
        value = event.target.getAttribute('value');
        title = event.target.innerText;
        this.props.callBack(value, title);
    },

    render: function() {
        var content = <LoadingBar />;
        if (this.state.loaded)
        {
            content = this.state.data.results.map(function (object) {
                    return (
                        <li key={object.id} value={this.props.childType+object.id} onClick={this.handleClick}>
                            {object.title}
                        </li>);
                }.bind(this));
        }
        return (
            <ul>
                {content}
            </ul>
        );
    }
});



var InnerSearchArea = React.createClass({
    getInitialState: function() {
        return {
            current_link: 'H',
            p: {'id':undefined, 'title':undefined},
            c: {'id':undefined, 'title':undefined},
            t: {'id':undefined, 'title':undefined}
        };
    },

    handleChange: function(value, title) {
        state = this.state;
        state.current_link = value[0];
        id = value.substring(1);
        if(value[0]=='P') {
            state.p.id = id;
            state.p.title = title;
        }
        else if(value[0]=='C') {
            state.c.id = id;
            state.c.title = title;
        }
        else if(value[0]=='T') {
            state.t.id = id;
            state.t.title = title;
        }
        this.setState(state);
    },

    handleClick: function(event) {
        value = event.target.getAttribute('value');
        state = this.state;
        state.current_link = value[0];
        this.setState(state);
    },

    render: function() {
        var content = '';
        var home = <li onClick={this.handleClick}><a value='H' href="#">Home</a></li>;
        var p = '';
        var c = '';
        var t = '';
        if(this.state.current_link == 'H') {
            content = <List childType='P' url='parent_category/?' callBack={this.handleChange}/>;
            home = <li class='active'>Home</li>;
        }
        else if(this.state.current_link == 'P') {
            content = <List childType='C' url={'category/?parent='+this.state.p.id+'&'} callBack={this.handleChange}/>;
            p = <li class='active'>{this.state.p.title}</li>;
        }
        else if(this.state.current_link == 'C') {
            content = <List childType='T' url={'course/?category='+this.state.c.id+'&'} callBack={this.handleChange}/>;
            p = <li onClick={this.handleClick}><a value='P' href="#">{this.state.p.title}</a></li>;
            c = <li class="active">{this.state.c.title}</li>;
        }
        else if(this.state.current_link == 'T') {
            content = <SearchGroups id={this.state.t.id}/>;
            p = <li onClick={this.handleClick} value=''><a value='P' href="#">{this.state.p.title}</a></li>;
            c = <li onClick={this.handleClick}><a value='C' href="#">{this.state.c.title}</a></li>;
            t = <li class='active'>{this.state.t.title}</li>;
        }
        return (
            <div class='panel panel-default'>
                <div class='panel-heading heading-inner-search-area'>
                    <div class='row'>
                        <div class='col-md-11'>
                        <ol class="breadcrumb bread-crumb-search-area">
                            {home}{p}{c}{t}
                        </ol>
                        </div>
                        <button class='btn btn-default btn-sm btn-inner-search-area' data-toggle='collapse' data-parent='#search-area' data-target='#searchable-area'>
                        <span class='glyphicon glyphicon-chevron-down' />
                        </button>
                    </div>
                </div>
                <div id='searchable-area' class='panel-collapse collapse'>
                    {content}
                </div>
            </div>
        );
    }
});



/*
    This class contains the shortlisted courses from which data is to be copied
    to the syllabus
*/
var Shortlisted = React.createClass({
    mixins: [LoadMixin],
    getUrl: function() {
        return '/courseware/api/offering/' + this.props.courseid + '/get_shortlisted_courses/?format=json';
    },

    componentWillReceiveProps: function(nextProps) {
        state = this.state;
        state.loaded = false;
        state.data = undefined;
        this.setState(state, this.loadData);
    },

    render: function() {
        var content = '';
        if (this.state.loaded)
        {
            content = this.state.data.map(function (course) {
                    return <div>{course.title}</div>;
                }.bind(this));
        }
        return (
            <div>
                {content}
            </div>
        );
    }
});



/*
    This class defines the left handside of the syllabus box.
    This class handles the search area from which data will be presented to be included
    in the syllabus.
    Structure:

    SearchArea [R]
        Heading
        Shortlisted Courses[R]
        InnerSearchArea [R]
*/
var SearchArea = React.createClass({
    render: function() {
        return (
            <div>
                <h3 class='center'>
                    Search Area
                </h3>
                <div class='panel-group' id='search-area'>
                    <div class='panel panel-default'>
                        <div class='panel-heading' data-toggle='collapse' data-parent='#search-area' data-target='#shortlisted'>
                            Shortlisted Courses
                        </div>
                        <div id='shortlisted' class='panel-collapse collapse'>
                            <Shortlisted courseid={this.props.id}/>
                        </div>
                    </div>
                    <InnerSearchArea />
                </div>
            </div>
        );
    }
});



/*
    This class defines the structure of the syllabus box.
    Structure:

    SearchArea[R]    Syllabus[R]
*/
var SyllabusStructure = React.createClass({
    render: function() {
        return (
            <div>
                <div class='col-md-6'>
                    <SearchArea id={this.props.id}/>
                </div>
                <div class='col-md-6'>
                    <Syllabus id={this.props.id}/>
                </div>
            </div>
        );
    }
});