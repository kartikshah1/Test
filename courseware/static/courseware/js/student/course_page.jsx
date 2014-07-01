/** @jsx React.DOM */

var Section = React.createClass({
    render: function() {
        return (
            <div class="section">
                <div>
                    <h4>
                        {this.props.section.title}
                    </h4>
                    <p><span dangerouslySetInnerHTML={{__html: converter.makeHtml(this.props.section.description)}} /></p>
                </div>
            </div>
        );
    }
});

var Page = React.createClass({

    loadPage: function() {
        url = "/document/api/page/" + this.props.id + "/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.setState({content: response, loaded: true});
        }.bind(this));
    },

    getInitialState: function() {
        return {
            loaded: false,
            content: undefined,
        };
    },

    componentDidMount: function() {
        if (!this.state.loaded) {
            this.loadPage();
        }
    },

    componentDidUpdate: function() {
        if (!this.state.loaded) {
            this.loadPage();
        }
    },

    componentWillReceiveProps: function() {
        this.setState({
            loaded: false,
            content: undefined,
        });
    },

    render: function() {
        if (!this.state.loaded) {
            return (
                <LoadingBar />
            );
        }
        else {
            var sections = this.state.content.sections.map(function (section) {
                return (
                    <Section section={section}/>
                );
            }.bind(this));
            return (
                <div class="mydocument">
                    <h3>{this.state.content.title}</h3>
                    <p><span dangerouslySetInnerHTML={{__html: converter.makeHtml(this.state.content.description)}} />
                    </p>
                    <div>
                        {sections}
                    </div>
                </div>
            );
        }
    }
});