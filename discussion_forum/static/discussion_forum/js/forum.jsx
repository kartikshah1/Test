/** @jsx React.DOM */


// Badge Choices: Must be same as in discussion_forum/models.py
BADGE_CHOICES = {
    'CT': 'Course Staff',
    'IN': 'Instructor',
    'MO': 'Moderator',
    'ST': 'Student',
    'TA': 'Teaching Assistant',
    'AN': 'Anonymous'
};

var SearchBar = React.createClass({

    getUrl: function() {
        return "/forum/api/forum/" + this.props.id + "/search_threads/";
    },
    searchForum: function() {
        search_url = this.getUrl();
        var search_str = this.refs.search.getDOMNode().value.trim();
        search_str = encodeURIComponent(search_str);
        request = ajax_json_request(search_url+"?search="+ search_str +"&format=json", "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
        }.bind(this));
    },

    render: function() {
        return (
        <div class="input-group col-md-4">
            <input type="text" ref="search" placeholder="Search here" class="form-control" />
            <span class="input-group-btn">
                <button class="btn btn-default" type="button" onClick={this.searchForum}>
                    <span class="glyphicon glyphicon-search"></span>
                </button>
            </span>
        </div>
    );
}
});


var TagList = React.createClass({
updateUrl: function() {
    var list = this.refs.tags.getDOMNode();
    var id = $(list).find('option:selected').prop('value');
    var url = "/forum/api/";
    if(id == -1) {
        url += "forum/" + this.props.id;
    } else {
        //url += "forum/" + this.props.id;
        url += "tag/" + id;
    }

    url += "/threads/?format=json";
    this.props.load(url);
},

render: function() {
    var options = this.props.tags.map(function(tag) {
        return <option key={"thread_tags_" + tag.id} value={tag.id}>{tag.title}</option>;
    });
    return (
        <div class="input-group col-md-3">
            <select ref="tags" class="form-control" onChange={this.updateUrl}>
                <option value={-1}>All Threads</option>
                {options}
            </select>
        </div>
    );
}
});


var SortOrders = React.createClass({
setToRecent: function() {
    this.props.order("recent");
},

setToEarlier: function() {
    this.props.order("earlier");
},

setToPopularity: function() {
    this.props.order("popularity");
},

render: function() {
    return (
        <div class="btn-group sort-orders" data-toggle="buttons">
            <label class="btn btn-xs btn-default active" onClick={this.setToRecent}>
                <input type="radio" name="options" id="option1" /> Recent
            </label>
            <label class="btn btn-xs btn-default" onClick={this.setToEarlier}>
                <input type="radio" name="options" id="option2" /> Earlier
            </label>
            <label class="btn btn-xs btn-default" onClick={this.setToPopularity}>
                <input type="radio" name="options" id="option3" /> Popularity
            </label>
        </div>
    );
}
});


/*
*  Thread's Tag + Subscription Funcationality UI Elements
*
*/
var ForumTag = React.createClass({
add: function() {
    this.props.add(this.props.data.id);
},

render: function() {
    return (
        <li><a onClick={this.add}>{this.props.data.title}</a></li>
    )
}
});

var ThreadTag = React.createClass({
remove: function() {
    this.props.remove(this.props.data.id);
},

render: function() {
    return (
        <div class="label label-info thread-tag">
            <span class="thread-tag-text">{this.props.data.title}</span>
            <a class="glyphicon glyphicon-remove-circle" onClick={this.remove}></a>
        </div>
    )
}
});

var ThreadTagList = React.createClass({
getInitialState: function(id) {
    return {"tags": this.props.thread_tags} ;
},

getUrl: function(_type) {
    return "/forum/api/thread/" + this.props.thread_id + "/" + _type + "/?format=json";
},

handleSubmit: function(_type, id) {
    var _url = this.getUrl(_type);
    var data = {"value": id};
    request = ajax_json_request(_url, "POST", data);
    request.done(function(response) {
        response = jQuery.parseJSON(response);
        this.setState({"tags": response});
    }.bind(this));
},

removeThreadTag: function(id) {
    this.handleSubmit("remove_tag", id);
},

addThreadTag: function(id) {
    this.handleSubmit("add_tag", id);
},

render: function() {
    var mdata = {"title": "hello hasan"};

    var threadTags = this.state.tags.map(function (tag) {
        return <ThreadTag key={"thread_tag_"+this.props.thread_id+"_"+tag.id} data={tag} remove={this.removeThreadTag} />;
    }.bind(this));

    var forumTags = this.props.forum_tags.map(function (tag) {
        return <ForumTag key={"forum_thread_tag_"+this.props.thread_id+"_"+tag.id} data={tag} add={this.addThreadTag} />;
    }.bind(this));

    return (
        <div class="thread-tag-list">
            <span class="thread-tag-list-label"> Tags: </span>
            {threadTags}
            <div class="btn-group btn-xs">
                <button type="button" class="btn btn-default thread-tag-add dropdown-toggle glyphicon glyphicon-plus" data-toggle="dropdown">
                </button>
                <ul class="dropdown-menu forum-tags" role="menu">
                    {forumTags}
                </ul>
            </div>
        </div>
    )
}
});


var ThreadSubscription = React.createClass({
getInitialState: function() {
    return {"subscribed": this.props.subscribed}
},

getUrl: function(_type) {
    return "/forum/api/thread/" + this.props.thread_id + "/" + _type + "/?format=json";
},

handleSubmit: function(_type) {
    var _url = this.getUrl(_type);
    var request = ajax_json_request(_url, "GET", {});
    request.done(function(response) {
        response = jQuery.parseJSON(response);
        this.setState({"subscribed": response.subscribed});
    }.bind(this));
},

subscribe: function() {
    this.handleSubmit("subscribe");
},

unsubscribe: function() {
    this.handleSubmit("unsubscribe");
},

render: function() {
    if(this.state.subscribed) {
        return (
            <a class="thread-subscribe-link" onClick={this.unsubscribe} data-toggle="tooltip" title="Click to stop recieving updates">Unsubscribe</a>
        )
    } else {
        return (
            <a class="thread-subscribe-link" onClick={this.subscribe} data-toggle="tooltip" title="Get Instant updates about this thread">Subscribe</a>
        )
    }
}
});





var ThreadForm = React.createClass({
mixins: [FormMixin],

handleSubmit: function() {
    var form_data = {
        "title": this.refs.title.getDOMNode().value.trim(),
        "content": this.refs.content.getDOMNode().value.trim(),
        "anonymous": this.refs.anonymous.getDOMNode().checked,
        "subscribe": this.refs.subscribe.getDOMNode().checked,
        "tag_id": this.refs.add_tags.getDOMNode().value.trim()
    }

    if(!form_data["title"] || !form_data["content"]) {
        return false;
    }
    this.props.submit(form_data);
    this.refs.title.getDOMNode().value = '';
    this.refs.content.getDOMNode().value = '';
    this.refs.anonymous.getDOMNode().value = false;
    this.refs.subscribe.getDOMNode().value = true;
    this.removeForm();
    return false;
},


render: function() {
    if (this.state.loaded) {
    var options = this.props.tags.map(function(tag) {
        return <option key={"thread_tags_" + tag.id} value={tag.id}>{tag.title}</option>;
    });
        content = (
            <form id="thread-submit-form" class="well" >
                <button type="button" class="close" aria-hidden="true" onClick={this.removeForm} >&times;</button>
                <h4>Start new Thread</h4>
                <input type="text" class="form-control" ref="title" placeholder="Thread Title" />
                <div>
                    <div class="wmd-toolbox"></div>
                    <WmdTextarea ref="content" placeholder="Add description here..." />
                </div>
                <div class="checkbox">
                    <label>
                        <input type="checkbox" ref="anonymous" />
                        Post as Anonymous {this.props.url}
                    </label>
                </div>
                <div>
                    <label>Category:
                        <select ref="add_tags" class="form-control">
                            {options}
                      </select>
                    </label>
                </div>
                <div class="checkbox">
                    <label>
                        <input type="checkbox" ref="subscribe" checked />
                        Post and Subscribe to Thread Updates. (No emails)
                    </label>
                </div>
                <button class="btn btn-primary col-md-3" onClick={this.handleSubmit}>Submit</button>
            </form>
        );
    } else {
        content = <button class="btn btn-primary" onClick={this.loadForm}>Add new Thread</button>;
    }
    return (
        <div>{content}</div>
    );
}
});


var ContentForm = React.createClass({
mixins: [FormMixin],

handleSubmit: function() {
    var form_data = {
        "content": this.refs.content.getDOMNode().value.trim(),
        "anonymous": this.refs.anonymous.getDOMNode().checked
    }

    if(!form_data["content"]) {
        return false;
    }

    this.props.submit(form_data);

    this.props.callback(1);

    this.refs.content.getDOMNode().value = '';
    this.refs.anonymous.getDOMNode().value = false;

    this.removeForm();
    return false;
},

render: function() {
    var content;
    if (this.state.loaded) {
        content = (
            <form>
                <button type="button" class="close content-form-close" aria-hidden="true" onClick={this.removeForm} >&times;</button>
                <WmdTextarea ref="content" placeholder={"Add a " + this.props.type + "..."} />
                <div class="content-form">
                    <button onClick={this.handleSubmit} class="content-form-btn btn btn-primary btn-sm col-md-2">Add {this.props.type}</button>
                    <div class="checkbox col-md-4">
                        <label>
                            <input type="checkbox" ref="anonymous" />
                            Post as Anonymous
                        </label>
                    </div>
                </div>
            </form>
        );
    } else {
        content = <button onClick={this.loadForm} class="content-form-btn btn btn-default btn-sm col-md-2">Make {this.props.type}</button>;
    }
    return (
        <div class="content-form">
            {content}
        </div>
    )
}
});


var VoteObject = React.createClass({
render: function() {
    return (
        <span href="#" onClick={this.props.onClick} class="vote-object" data-toggle="tooltip" title="first tooltip">
            <span class={"glyphicon glyphicon-" + this.props.type}></span>{' '}{this.props.val}
        </span>
    );
}
});


var ContentMetaInfo = React.createClass({
getUrl: function(_name) {
    var str = ((_name == null) ? '' : "/" + _name);
    var _url = "/forum/api/content/" + this.props.data.id + str + "/?format=json";
    return _url;
},

query: function(url) {
    request = ajax_json_request(url, "GET", {});
    request.done(function(response) {
        item = jQuery.parseJSON(response);
        this.props.callback(item);
    }.bind(this));
},

upvote: function() {
    this.query(this.getUrl("upvote"));
},

downvote: function() {
    this.query(this.getUrl("downvote"));
},

markSpam: function() {
    this.query(this.getUrl("mark_spam"));
},

editContent: function() {
    this.props.edit();
},

deleteContent: function() {
    request = ajax_json_request(this.getUrl(null), "DELETE", {});
    request.done(function(response) {
        display_global_message("Content deleted", "info");
        this.props.remove();
    }.bind(this));
},

pinContent: function() {
    this.query(this.getUrl("pin_content"));
},

disableContent: function() {
    request = ajax_json_request(this.getUrl("disable"), "GET", {});
    request.done(function(response) {
        item = jQuery.parseJSON(response);
        display_global_message("Content disabled", "info");
        this.props.remove();
    }.bind(this));
},

enableContent: function() {
    this.query(this.getUrl("enable"));
},

render: function() {
    if (this.props.type == "reply") {
        comment = '';
    } else {
        comment = <li><span class="glyphicon glyphicon-comment"></span>{' ' + this.props.data.children_count}</li>;
    }

    var pinned = '';
    if(this.props.data.pinned) {
        pinned = <li><span class="glyphicon glyphicon-pushpin"></span></li>;
    }

    var is_author = ((this.props.data.author == null)?
                        false :
                        (this.props.data.author.id == this.props.current_user.user.id));
    var is_moderator = (this.props.current_user.moderator || this.props.current_user.super_user);

    var edit_option = (
        <li key={"content_"+this.props.data.id+"_edit"}><a onClick={this.editContent}><span class="glyphicon glyphicon-edit"></span>&nbsp;&nbsp;Edit</a></li>
    );

    var delete_option = (
        <li key={"content_"+this.props.data.id+"_delete"}><a onClick={this.deleteContent}><span class="glyphicon glyphicon-trash"></span>&nbsp;&nbsp;Delete</a></li>
    );

    var pin_option = (
        <li key={"content_"+this.props.data.id+"_pin"}><a onClick={this.pinContent}><span class="glyphicon glyphicon-pushpin"></span>&nbsp;&nbsp;Pin Content</a></li>
    );

    var disable_option = (
        <li key={"content_"+this.props.data.id+"_disable"}><a onClick={this.disableContent}><span class="glyphicon glyphicon-minus-sign"></span>&nbsp;&nbsp;Disable</a></li>
    );

    var dropdown_options;
    if (is_moderator) {
        dropdown_options = new Array(edit_option, delete_option, pin_option, disable_option);
    } else if(is_author) {
        dropdown_options = new Array(edit_option, delete_option);
    } else {
        dropdown_options = undefined;
    }

    var dropdown;
    if(dropdown_options != undefined) {
        dropdown = (
            <div class="btn-group btn-group-xs content-meta-btn">
                <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                    <span class="caret"></span>
                </button>
                <ul class="dropdown-menu">
                    {dropdown_options}
                </ul>
            </div>
        );
    } else {
        dropdown = (<span></span>);
    }

    return (
        <div>
            {dropdown}

            <ul class="content-meta-info">
                {pinned}
                <li>by - <UserLink data={this.props.data.author} /> </li>
                <li><span class="label label-default">{this.props.data.author_badge}</span></li>
                <li><DynamicDateTime time={this.props.data.created} refreshInterval={20000} /></li>
                {comment}
                <li><VoteObject onClick={this.upvote} type="thumbs-up" val={this.props.data.upvotes} /></li>
                <li><VoteObject onClick={this.downvote} type="thumbs-down" val={this.props.data.downvotes}/></li>
                <li><VoteObject onClick={this.markSpam} type="flag" val={this.props.data.spam_count}/></li>
            </ul>
        </div>
    );
}
});


var Content = React.createClass({
getInitialState: function() {
    return {edit: false};
},

getUrl : function() {
    return "/forum/api/content/" + this.props.data.id + "/?format=json";
},

componentDidMount: function(rootNode) {
    //$(rootNode).find(".content-meta-info").fadeTo(1,0);
    $(rootNode).find(".content-meta-btn").fadeTo(1,0);
    $(rootNode).hover(
        function() {
            //$(rootNode).find(".content-meta-info").fadeTo(1,1);
            $(rootNode).find(".content-meta-btn").fadeTo(1,1);
        },
        function() {
            //$(rootNode).find(".content-meta-info").fadeTo(1,0);
            $(rootNode).find(".content-meta-btn").fadeTo(1,0);
        }
    );
    //MathJax.Hub.Queue(["Typeset", MathJax.Hub, rootNode]);
},

// Load edit form
loadEditForm: function() {
    this.setState({edit: true});
},

// Removes the form and display data
removeEditForm: function() {
    this.setState({edit: false});
},

// Send PATCH request to server for updating content
submitEditForm: function() {
    var data = {
        "content": this.refs.content.getDOMNode().value.trim()
    }

    if(!data.content) {
        return false;
    }

    request = ajax_json_request(this.getUrl(), "PATCH", data);
    request.done(function(response) {
        item = jQuery.parseJSON(response);
        this.props.callback(item);
        this.removeEditForm();
    }.bind(this));
    return false;
},

render: function() {
    if (this.state.edit) {  //Render edit form
        return (
            <form>
                <button type="button" class="close content-form-close" aria-hidden="true" onClick={this.removeEditForm} >&times;</button>
                <WmdTextarea ref="content" placeholder="Edit Content" defaultValue={this.props.data.content} />
                <div class="content-form">
                    <button onClick={this.submitEditForm} class="content-form-btn btn btn-primary btn-sm col-md-2">Update</button>
                </div>
            </form>
        )
    }

    var rawMarkup = converter.makeHtml(this.props.data.content);
    return (
        <div class={"content " + this.props.type}>
            <p>
                <span dangerouslySetInnerHTML={{__html: rawMarkup}} />
            </p>
            <div class="content-meta-info-container">
                <ContentMetaInfo current_user={this.props.current_user} type={this.props.type} data={this.props.data} callback={this.props.callback} remove={this.props.remove} edit={this.loadEditForm} />
            </div>
        </div>
    )
}
});


var ForumUserSetting = React.createClass({
getInitialState: function() {
    return {"subscribed": this.props.data.email_digest};
},

handleSubmit: function() {
    var mark = ((this.state.subscribed) ? false : true);
    var data = {"email_digest": mark};
    var _url = "/forum/api/user_setting/" + this.props.data.id + "/?format=json";
    var request = ajax_json_request(_url, "PATCH", data);
    request.success(function(response) {
        response = jQuery.parseJSON(response);
        this.setState({"subscribed": response.email_digest});
    }.bind(this));
},

render: function() {
    var text = "";
    if(this.state.subscribed) {
        text = (<span><span class="glyphicon glyphicon-ok"></span> You are Subscribed for daily Email Digest</span>);
    } else {
        text = (<span>Subscribe for daily Email Digest</span>);
    }
    return (
        <div class="btn-group pull-right">
            <button type="button" class="btn btn-default btn-sm dropdown-toggle" data-toggle="dropdown">
                <span class="glyphicon glyphicon-cog"></span>
            </button>
            <ul class="dropdown-menu forum-tags" role="menu">
                <li role="presentation" class="dropdown-header">Forum Settings</li>
                <li><a onClick={this.handleSubmit}>{text}</a></li>
            </ul>
        </div>
    )
}
});


var Forum = React.createClass({
getUrl: function() {
    return "/forum/api/forum/" + this.props.id + "/";
},

getThreadUrl: function() {
    return "/forum/api/thread/" + this.props.id + "/";
},

getInitialState: function() {
    forum_url = "/forum/api/forum/" + this.props.id + "/";
    new_state = {
        "add_tag_url":  forum_url + "add_tag/?format=json",
        "activity_url": forum_url + "activity/?format=json",
        "threads_url": forum_url + "threads/?format=json",
        "add_thread_url": forum_url + "add_thread/?format=json",
        "review_content_url": forum_url + "review_content/?format=json",
        "search_url": forum_url + "search_threads/",
        "data": {},
        "loaded": false,
        "user_setting": {}
    };

    // Loading forum_state dynamically
    this.loadUserSetting();
    this.loadForum();
//    this.loadTags();

    return new_state;
},

loadUserSetting: function() {
    setting_url = this.getUrl() + "user_setting/?format=json";
    request = ajax_json_request(setting_url, "GET", {});
    request.done(function(response) {
        response = jQuery.parseJSON(response);
        var state = this.state;
        state.user_setting = response;
        this.setState(state);
    }.bind(this));
},

loadTags: function(){
    url = this.getThreadUrl()+  "get_tag_list/?format=json";
    request = ajax_json_request(url, "GET", {});
    request.done(function(response) {
        response = jQuery.parseJSON(response);
        var state = this.state;
        state.data.tags = response['results'];
        state.loaded = true;
        this.setState(state);
    }.bind(this));
},

loadForum: function() {
    forum_url = this.getUrl();
    request = ajax_json_request(forum_url+"?format=json", "GET", {});
    request.done(function(response) {
        response = jQuery.parseJSON(response);
        var state = this.state;
        state.data = response;
        state.loaded = true;
        this.setState(state);
    }.bind(this));
},

updateThreadUrl: function(url) {
    var state = this.state;
    state.threads_url = url;
    this.setState(state);
},

searchForum: function() {
    search_url = this.getUrl()+"search_threads/";
    var search_str = this.refs.search.getDOMNode().value.trim();
    search_str = encodeURIComponent(search_str);
    request = ajax_json_request(search_url+"?search="+ search_str +"&format=json", "GET", {});
    request.done(function(response) {
        response = jQuery.parseJSON(response);
        var state = this.state;
        state.data = response;
        this.setState(state);
    }.bind(this));
},

render: function() {
    if(!this.state.loaded) {
        return (<LoadingBar />);
    }

    return (
        <div class="panel panel-default">
            <div class="panel-heading forum-heading">
                <h3 class="pull-left">
                    Discussion Forum &nbsp;&nbsp;&nbsp;
                    <span class="forum-text-mute">Threads: {this.state.data.thread_count}</span>
                </h3>
                <ForumUserSetting data={this.state.user_setting} />
            </div>
            <div class="panel-body">
                <div class="row">
            <div class="input-group col-md-4">
                <input type="text" ref="search" placeholder="Search here" class="form-control" />
                <span class="input-group-btn">
                    <button class="btn btn-default" type="button" onClick={this.searchForum}>
                        <span class="glyphicon glyphicon-search"></span>
                    </button>
                </span>
            </div>
                        <TagList tags={this.state.data.tags} forum_id={this.state.data.id} load={this.updateThreadUrl}/>
                    </div>

                    <hr/>

                    <ThreadList list={this.state.threads_url} add={this.state.add_thread_url} add_tag={this.state.add_tag_url} forum_tags={this.state.data.tags} current_user={this.state.user_setting} />
                </div>
            </div>
        );
    }
});
