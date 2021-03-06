/** @jsx React.DOM */

var StudentPublicProgress = React.createClass({
    getInitialState: function() {
        return {
            course: this.props.id,
            id: this.props.student.id,
            name: this.props.student.name,
            user: this.props.student.user,
            max_score: this.props.student.max_score,
            score: this.props.student.score,
            groups: undefined,
            loaded: false
        };
    },
    componentWillReceiveProps: function(nextProps) {
        this.setState({
            course: nextProps.id,
            id: nextProps.student.id,
            name: nextProps.student.name,
            user: nextProps.student.user,
            max_score: nextProps.student.max_score,
            score: nextProps.student.score,
            groups: undefined,
            loaded: false,
        });
    },

    loadData: function(){
        if(!this.state.loaded){
            url = '/courseware/api/course/' + this.state.course + "/get_all_public_marks_student/?format=json&student=" + this.state.id;
            request = ajax_json_request(url, "GET", {});
            request.done(function(response) {
                response = jQuery.parseJSON(response);
                oldState = this.state;
                oldState = response;
                oldState.loaded = true;
                console.log(oldState);
                this.setState(oldState);
            }.bind(this));
        }
    },
    render: function() {
        var progressgroups = null
        if(this.state.loaded){
            progressgroups = this.state.groups.map(function (object) {
                return <ProgressGroup group={object} />;
            });
        }
        return (
            <div onClick={this.loadData} class='panel panel-default'>
                <div class='panel-heading' data-toggle='collapse' data-parent="#studentmarks"
                data-target={'#student-' + this.props.student.id}>
                    <div class="row panel-title">
                        <div class="col-md-3">
                            {this.props.student.user}
                        </div>
                        <div class="col-md-3">
                            {this.props.student.name}
                        </div>
                        <div class="col-md-3">
                            {this.props.student.score}
                        </div>
                        <div class="col-md-3">
                            {this.props.student.max_score}
                        </div>
                    </div>
                </div>
                <div id={'student-'+this.props.student.id} class='panel-collapse collapse'>
                    <div class="panel-body">
                        <div class='panel-group'>
                            {progressgroups}
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

PublicProgress = React.createClass({
    mixins: [LoadMixin, SortableMixin],

    dynamicSort: function(property) {
        var sortOrder = 1;
        if(property[0] === "-") {
            sortOrder = -1;
            property = property.substr(1);
        }
        return function (a,b) {
            var x = a[property];
            var y = b[property];
            if(isNaN(x)){
                x = x.toLowerCase();
                y = y.toLowerCase();
                var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
                return result * sortOrder;
            }else{
                x = +x;
                y = +y;
                var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
                return result * sortOrder;
            }
        }
    },

    sort: function(sortBy) {
        var that = this;
        return function(){
            oldState = that.state;
            if(oldState.sortBy == sortBy){
                oldState.data.students.sort(that.dynamicSort("-" + sortBy));
                oldState.sortBy = "-" + sortBy;
            }
            else{
                oldState.data.students.sort(that.dynamicSort(sortBy));
                oldState.sortBy = sortBy;
            }
            that.setState(oldState);
        };
    },

    getUrl: function() {
        return '/courseware/api/course/' + this.props.course + '/get_all_public_marks/?format=json';
    },

    render: function() {
        if (!this.state.loaded) {
            return <LoadingBar />;
        }
        var that = this;
        var studentmarks = this.state.data.students.map(function (object) {
            return <StudentPublicProgress student={object} id={that.props.course}/>;
        });
        var icon = {
            user: null,
            name: null,
            score: null,
            max_score: null
        }
        if(this.state.sortBy){
            if(this.state.sortBy[0] == "-"){
                icon[this.state.sortBy.substr(1)] = (<span class="glyphicon glyphicon glyphicon-chevron-down"></span>);
            }
            else{
                icon[this.state.sortBy] = (<span class="glyphicon glyphicon glyphicon-chevron-up"></span>);
            }
        }

        var showButton = <ShowProgressButton course={this.props.course} onChange={this.loadData}/>;

        return (
            <div class="row">
                <div class="row">
                    <h3 class="col-md-8">
                        Scorecard
                    </h3>
                    {showButton}
                </div>
                <div class="row panel-heading">
                    <div class="col-md-3">
                        <a href="#" onClick = {this.sort("user")}> Username </a>
                        {icon["user"]}
                    </div>
                    <div class="col-md-3">
                        <a href="#" onClick = {this.sort("name")}> Name </a>
                        {icon["name"]}
                    </div>
                    <div class="col-md-3">
                        <a href="#" onClick={this.sort("score")}> Score </a>
                        {icon["score"]}
                    </div>
                    <div class="col-md-3">
                        <a href="#" onClick={this.sort("max_score")}> Max Score </a>
                        {icon["max_score"]}
                    </div>
                </div>
                <div class='panel-group' id='studentmarks'>
                    {studentmarks}
                </div>
            </div>
        );
    }
});

ShowProgressButton = React.createClass({
    mixins: [LoadMixin],

    getUrl: function() {
        return '/courseware/api/course/' + this.props.course + '/get_marks_setting/?format=json';
    },

    change_setting: function(){
        var show = (this.state.data? "false": "true");
        url = '/courseware/api/course/' + this.props.course + "/set_marks_setting/?format=json&show=" + show;
        request = ajax_json_request(url, "PATCH", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.data = response;
            this.setState(oldState);
            this.props.onChange();
        }.bind(this));
    },

    render: function(){
        var show = this.state.data;
        var buttonShow;
        if(show!=true){
            buttonShow = (<div class="col-md-2 col-md-offset-1  showmarksbutton">
                <button class="btn btn-primary" type="button" onClick={this.change_setting}>Show Marks to Public</button>
            </div>);
        }
        else{
            buttonShow = (<div class="col-md-2 col-md-offset-1  showmarksbutton">
                <button class="btn btn-danger" type="button" onClick={this.change_setting}>Hide Marks from Public</button>
            </div>);
        }
        return(
            <div class="row">
                {buttonShow}
            </div>
        );
    }
});