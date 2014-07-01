/** @jsx React.DOM */

/*
Common Functionality for updating state of thread/comment/reply objects
*/
var ContentUpdateMixin = {
    updateContentData: function(new_data) {
        //Update thread-meta info
        // We are not using title and tags in state
        this.setState({data: new_data});
    },

    updateChildrenCount: function(val) {
        var state = this.state;
        if(state.data == null) {
            return;
        }
        state.data.children_count += val;  // We are not using title and tags in state
        this.setState(state);
    },

    remove: function() {
        var state = this.state;
        state.deleted = true;
        this.props.callback(-1);
        this.setState(state);
    }
};


/*
    Abstracted common functionality of ThreadForm and ContentForm
*/
var FormMixin = {
    getInitialState: function() {
        return {loaded: false};
    },

    loadForm: function() {
        this.setState({loaded: true});
    },

    removeForm: function() {
        this.setState({loaded: false});
    }
};


/*
    Abstracted common functionality of ThreadList, CommentList, ReplyList
*/
var ListMixin = {
    // Requied props: list, add (only if submit is allowed)
    getInitialState: function() {
        return {
            count: 0,   //Count of total items in database
            next: this.props.list,
            items: []
        };
    },

    addItem: function(item) {
        var items = this.state.items;
        if(this.props.push == "front") {
            items.unshift(item);
        } else {
            items.push(item);
        }
        var new_state = {
            "count": this.state.count + 1,
            "next": this.state.next,
            "items": items
        };
        this.setState(new_state);
    },

    updateState: function(response) {
        //Updates state after it gets list from server
        var items = this.state.items;
        items = items.concat(response.results);
        var new_state = {
            "count": response.count + this.state.count,
            "next": response.next,
            "items": items
        };
        this.setState(new_state);
    },

    loadMoreObjects: function(_url) {
        var data = {};
        var request = ajax_json_request(_url, "GET", data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.updateState(response);
        }.bind(this));
    },

    loadMore: function() {
        if (this.state.next == null) {
            return;
        }
        this.loadMoreObjects(this.state.next);
    },

    componentDidMount: function() {
        // Loads threads for the first time when component get mounted
        this.loadMoreObjects(this.state.next);
    },

    componentWillReceiveProps: function (nextProps) {
        /* Whenever list property is updated reset everything and load new \
         * threads
         */
        if(this.props.list == nextProps.list) {
            return;
        }

        var _url_part = ((this.order == undefined) ? '' : '&order='+this.order);

        var new_state = this.state;
        new_state.count = 0;   //Count of total items in database
        new_state.next = nextProps.list + _url_part;
        new_state.items = [];
        this.setState(new_state, this.loadMoreObjects(new_state.next));
    },

    updateSortOrder: function(order) {
        this.order = order;
        var new_state = {
            "count" : 0,
            "next": this.props.list + "&order="+ order,
            "items": [],
        }
        this.setState(new_state, this.loadMoreObjects(new_state.next));
    },

    submitContentForm: function(data) {
        //Make a json call for validation
        request = ajax_json_request(this.props.add, "POST", data);
        request.done(function(response) {
            item = jQuery.parseJSON(response);
            if("tag_id" in data)
                    {
               this.addTag(item['id'],data["tag_id"]);
            }
            this.addItem(item);
        }.bind(this));
    },

    addTag: function(id, value){
        url = "/forum/api/thread/"+id+"/add_tag/?format=json";
        data = {'value': value};
        request = ajax_json_request(url, "POST", data);
        request.done(function(response) {
            item = jQuery.parseJSON(response);
        }.bind(this));
    }
};
