/** @jsx React.DOM */

var Progress = React.createClass({
    mixins: [LoadMixin],

    getUrl: function() {
        return '/courseware/api/course/' + this.props.course + '/progress?format=json';
    },

    render: function() {
        if (!this.state.loaded) {
            return <LoadingBar />;
        }
        var progressgroups = this.state.data.groups.map(function (object) {
            return <ProgressGroup group={object} />;
        }.bind(this));
        var progressbar = 'Not Applicable';
        if (parseInt(this.state.data.max_score) != 0) {
            widthvalue = parseFloat(this.state.data.score)*100.0/parseFloat(this.state.data.max_score);
            progressbar = (
                <div class="col-md-8 progress no-padding">
                    <div class="progress-bar progress-bar-success" style={{'width': widthvalue+'%'}}>
                    <span class='progressbar-text'>{this.state.data.score}/{this.state.data.max_score}</span>
                    </div>
                    <div class="progress-bar progress-bar-warning" style={{'width': '0%'}}>
                    </div>
                </div>
            );
        }
        return (
            <div class="row">
                <h3>
                    My Progress
                </h3>
                <div class="row">
                    <div class="col-md-4">
                        Overall Progress
                    </div>
                    {progressbar}
                </div>
                <div class='panel-group' id='progressgroups'>
                    {progressgroups}
                </div>
            </div>
        );
    }
});