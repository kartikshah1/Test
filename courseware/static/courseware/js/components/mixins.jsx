/** @jsx React.DOM */

var EditableMixin = {
    handleEditClick: function() {
        oldState = this.state;
        oldState['showform'] = true;
        this.setState(oldState);
    },

    handleCancelEdit: function() {
        oldState = this.state;
        oldState['showform'] = false;
        this.setState(oldState);
    },

    toggleEdit: function() {
        oldState = this.state;
        oldState['showform'] = ! oldState['showform'];
        this.setState(oldState);
    }
};

var SortableMixin = {
    handleSortClick: function(id, myclass) {
        $(id).sortable({
            axis: 'y',
            cursor: "move",
            //containment: "parent",
            items: myclass,
            placeholder: "state-highlight",
            forcePlaceholderSize: true,
            start: function( event, ui ) {
                $(ui.item).addClass("state-movable");
            },
            stop: function( event, ui ) {
                $(ui.item).removeClass("state-movable");
            }
        });
        $(id).sortable("enable");
        //$(id).disableSelection();
        oldState = this.state;
        oldState['order'] = true;
        this.setState(oldState);
    },

    handleSaveOrder: function(id, keylength) {
        v = $(id).sortable("toArray");
        a = v.length;
        for(i=0; i< a;i++){
            v[i]=v[i].substring(keylength);
            v[i]=parseInt(v[i]);
        }
        data = {
            playlist: JSON.stringify(v)
        }
        this.saveOrder(data);
    },

    saveOrderSuccess: function(id) {
        $(id).sortable("disable");
        oldState = this.state;
        oldState['order'] = false;
        this.setState(oldState);
    }
};

var LoadMixin = {
    componentWillMount: function() {
        loaded = false;
        data = undefined;
        this.setState({loaded: loaded, data: data}, this.loadData);
    },

    /*componentDidMount: function() {
        if(!this.state.loaded){
            this.loadData();
        }
    },*/

    /*componentWillReceiveProps: function(nextProps) {
        state = this.state;
        state.loaded = false;
        state.data = undefined;
        this.setState(state, this.loadData);
    },*/

    componentDidUpdate: function() {
        if(!this.state.loaded){
            this.loadData();
        }
    },

    loadData: function() {
        request = ajax_json_request(this.getUrl(), "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            state = this.state;
            state['loaded'] = true;
            state['data'] = response;
            this.setState(state);
        }.bind(this));
        request.fail(function(response) {
            console.log("Load data failed for " + this.getUrl());
            console.log(response);
        }.bind(this));
    }
}

var ScrollToElementMixin = {
    componentDidMount: function() {
        $(this.getDOMNode()).hide().fadeIn();
        $('html,body').animate({
            scrollTop: $(this.getDOMNode()).offset().top - 100
        }, 1000).bind(this);
    }
}