/** @jsx React.DOM */

var ProgressConcept = React.createClass({
    render: function() {
        var progressbar = 'Not Applicable';
        if (parseInt(this.props.concept.max_score) != 0) {
            widthvalue = parseFloat(this.props.concept.score)*100.0/parseFloat(this.props.concept.max_score);
            progressbar = (
                <div class="col-md-8 progress no-padding">
                    <div class="progress-bar progress-bar-success" style={{'width': widthvalue+'%'}}>
                    <span class='progressbar-text'>{this.props.concept.score}/{this.props.concept.max_score}</span>
                    </div>
                    <div class="progress-bar progress-bar-warning" style={{'width': '0%'}}>
                    </div>
                </div>
            );
        } 
        return (
            <div class="row">
                <div class="col-md-4">
                    {this.props.concept.title}
                </div>
                {progressbar}
            </div>
        );
    }
});


var ProgressGroup = React.createClass({
    render: function() {
        var concepts = this.props.group.concepts.map(function (object) {
            return <ProgressConcept concept={object} />;
        });
        var progressbar = "Not Applicable";
        if (parseInt(this.props.group.max_score) != 0) {
            widthvalue = parseFloat(this.props.group.score)*100.0/parseFloat(this.props.group.max_score);
            progressbar = (
                <div class="col-md-8 progress no-padding">
                    <div class="progress-bar progress-bar-success" style={{'width': widthvalue+'%'}}>
                    <span class='progressbar-text'>{this.props.group.score}/{this.props.group.max_score}</span>
                    </div>
                    <div class="progress-bar progress-bar-warning" style={{'width': '0%'}}>
                    </div>
                </div>
            );
        }
        return (
            <div class='panel panel-default'>
                <div class='panel-heading' data-toggle='collapse' data-parent="#progressgroups" 
                data-target={'#progress-group-' + this.props.group.id}>
                    <div class="row panel-title">
                        <div class="col-md-4">
                            {this.props.group.title}
                        </div>
                        {progressbar}
                    </div>
                </div>
                <div id={'progress-group-'+this.props.group.id} class='progress-group-collapse-box panel-collapse collapse'>
                    <div class="panel-body">
                        <div class='panel-group progress-concepts'>
                            {concepts}
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});
