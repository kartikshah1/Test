/** @jsx React.DOM */


var ForumSetting = React.createClass({
    getInitialState: function() {
        return {
            created: this.props.data.created,
            review_threshold: this.props.data.review_threshold,
            abuse_threshold: this.props.data.abuse_threshold
        };
    },

    componentDidMount: function() {
        $(".forum-a-link").tooltip();
    },

    updateSetting: function() {
        var data = {
            review_threshold: this.refs.review.getDOMNode().value.trim(),
            abuse_threshold: this.refs.abuse.getDOMNode().value.trim(),
        };

        var url = this.props.getUrl() + "?format=json";
        var request = ajax_json_request(url, 'PATCH', data);
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            var state = this.state;
            state.created = response.created;
            state.review_threshold = response.review_threshold;
            state.abuse_threshold = response.abuse_threshold;
            this.setState(state);
            display_global_message("Successfully updated thresholds", "success");
        }.bind(this));
    },

    render: function() {
        if(!this.props.selected) {
            return (<div></div>);
        }

        return (
            <table class="table forum-setting">
                <tr>
                    <td class="content-left">Created : </td>
                    <td>{moment(this.state.created).format('MMMM Do YYYY')}</td>
                </tr>
                <tr>
                    <td class="content-left">
                        <span class="forum-a-link" data-toggle="tooltip" title="Number of spam flags after which a particular content will be displayed for review. But it will still be visible to forum users" >
                           Review Threshold :
                        </span>
                    </td>
                    <td><input type="text" class="form-control" ref="review" defaultValue={this.state.review_threshold}/>
                    </td>
                </tr>
                <tr>
                    <td class="content-left">
                        <span class="forum-a-link" data-toggle="tooltip" title="Number of spam flags after which content will be disabled automatically. This number must be greater or equal to Review Threshold." >
                           Review Threshold :
                        </span>
                    </td>
                    <td><input type="text" class="form-control" ref="abuse" defaultValue={this.state.abuse_threshold}/>
                    </td>
                </tr>
                <tr>
                    <td class="content-left">

                    </td>
                    <td>
                        <div class="btn btn-default" onClick={this.updateSetting}>Update</div>
                    </td>
                </tr>
            </table>
        )
    }
});


var ForumTag = React.createClass({
    getUrl: function() {
        return "/forum/api/tag/" + this.state.data.id + "/?format=json";
    },

    getInitialState: function() {
        return {data: this.props.data};
    },

    toggleEdit: function() {
        var state = this.state;
        if(state.edit) {
            state.edit = false;
            this.updateTag();
        } else {
            state.edit = true;
        }
        this.setState(state);
    },

    updateTag: function() {
        var title = this.refs.title.getDOMNode().value.trim();
        var data = {"title": title};
        var url = this.getUrl();
        var request = ajax_json_request(url, "PATCH", data);
        request.success(function(response) {
            display_global_message("Tag title updated", "success");
        }.bind(this));
    },

    deleteTag: function() {
        var url = this.getUrl();
        var request = ajax_json_request(url, "DELETE", {});
        request.success(function(response) {
            display_global_message("Tag successfully deleted", "success");
            this.setState({deleted: true});
        }.bind(this));
    },

    render: function() {
        if(this.state.deleted) {
            return (<span></span>);
        }

        var title = '';
        var icon = '';
        if(this.state.edit) {
            icon = "saved";
            title = (<fieldset>
                        <input ref="title" type="text" class="form-control" placeholder="Title" defaultValue={this.state.data.title} />
                    </fieldset>);
        } else {
            icon = "edit";
            title = (<fieldset disabled>
                        <input ref="title" type="text" class="form-control" placeholder="Title" defaultValue={this.state.data.title} />
                    </fieldset>);
        }

        if(this.props.update) {
            var edit = (
                <span class="input-group-btn">
                    <button class="btn btn-default" type="button" onClick={this.toggleEdit}>
                        <span class={"glyphicon glyphicon-"+icon}></span>
                    </button>
                </span>
            );
            var deletebtn = (
                <span class="input-group-btn">
                    <button class="btn btn-danger" type="button" onClick={this.deleteTag}>
                        <span class="glyphicon glyphicon-trash"></span>
                    </button>
                </span>
            );
        } else {
            var edit = (<span></span>);
            var deletebtn = (<span></span>);
        }

        return (
            <div class="input-group col-md-6 admin-forum-tag">
                {edit}
                {title}
                {deletebtn}
            </div>
        )
    }
});


var ForumTags = React.createClass({
    getInitialState: function() {
        var state = {auto_tags:[], manual_tags:[]};
        var tags = this.props.tags;
        for(var i=0; i<tags.length; i++) {
            if(tags[i].auto_generated) {
                state.auto_tags.push(tags[i]);
            } else {
                state.manual_tags.push(tags[i]);
            }
        }
        return state;
    },

    addTag: function() {
        var url = this.props.getUrl() + "add_tag/?format=json";
        var title = this.refs.title.getDOMNode().value.trim();
        var data = {"title": title, "tag_name": title};
        var request = ajax_json_request(url, "POST", data);
        request.success(function(response) {
            tag = jQuery.parseJSON(response);
            var state = this.state;
            state.manual_tags.push(tag);
            this.setState(state);
        }.bind(this));

        this.refs.title.getDOMNode().value = '';
    },

    render: function() {
        if(!this.props.selected) {
            return <div></div>
        }

        var manual_tags = this.state.manual_tags.map(function(tag) {
            return (<ForumTag key={"forum_tag_"+tag.id} data={tag} update={true}/>);
        }.bind(this));

        var auto_tags = this.state.auto_tags.map(function(tag) {
            return (<ForumTag key={tag.id} data={tag} udpate={false}/>);
        }.bind(this));

        return (
            <div id="forum-tags-container">
                <h4>Add new Tag</h4>
                <div class="tag-container">
                    <div class="input-group col-md-7">
                        <input ref="title" type="text" class="form-control" placeholder="Write a meaningful Title" />
                        <span class="input-group-btn">
                            <button class="btn btn-default" type="button" onClick={this.addTag}>
                                Add New Tag
                            </button>
                        </span>
                    </div>
                </div>

                <h4>Generated Tags</h4>
                <div class="tag-container">
                    {manual_tags}
                </div>

                <h4>Auto Generated Tags</h4>
                <div class="tag-container">
                    {auto_tags}
                </div>
            </div>
        )
    }
});


var ForumUserSetting = React.createClass({
    getUrl: function() {
        return "/forum/api/user_setting/" + this.props.data.id + "/"
    },

    componentDidMount: function() {
        // Initializing data with appropriate values
        this.refs.email_digest.getDOMNode().checked = this.props.data.email_digest;
        this.refs.super_user.getDOMNode().checked = this.props.data.super_user;
        this.refs.moderator.getDOMNode().checked = this.props.data.moderator;

        var badges = this.refs.badges.getDOMNode();
        $(badges).val(this.props.data.badge);
    },

    updateModeration: function() {
        var mark = this.refs.moderator.getDOMNode().checked;

        var url = this.getUrl() + "update_moderation_permission/?format=json";
        var data = {"mark": mark};
        var request = ajax_json_request(url, "POST", data);
        request.success(function() {
            display_global_message("Moderation Permission updated !", "success");
        }.bind(this));
    },

    updateBadge: function() {
        var badges = this.refs.badges.getDOMNode();
        var badge = $(badges).find('option:selected').prop('value');

        var url = this.getUrl() + "update_badge/?format=json";
        var data = {"badge": badge};
        var request = ajax_json_request(url, "POST", data);
        request.success(function() {
            display_global_message("User Badge updated !", "success");
        }.bind(this));
    },

    render: function() {
        var choices = Object.keys(BADGE_CHOICES).map(function(key) {
            return <option value={key}>{BADGE_CHOICES[key]}</option>;
        }.bind(this));

        return (
            <tr>
                <td class="forum-admin-user-setting">
                    <UserLink data={this.props.data.user}/>
                </td>
                <td>
                    <div class="checkbox">
                        <label>
                            <input ref="email_digest" type="checkbox" disabled /><span> Email Digest</span>
                        </label>
                    </div>
                </td>
                <td>
                    <div class="checkbox">
                        <label>
                            <input ref="super_user" type="checkbox" disabled /><span> Super User</span>
                        </label>
                    </div>
                </td>
                <td>
                    <div class="checkbox">
                        <label>
                            <input ref="moderator" type="checkbox" onChange={this.updateModeration} /><span> Moderator</span>
                        </label>
                    </div>
                </td>
                <td>
                    <select ref="badges" class="form-control" onChange={this.updateBadge}>
                        {choices}
                    </select>
                </td>
            </tr>
        )
    }
});


var ForumUserList = React.createClass({
    mixins: [ListMixin],

    render: function() {
        var users = this.state.items.map(function(item) {
            return (<ForumUserSetting data={item} />);
        }.bind(this));
        if(this.state.items.length == 0) {
            users = (<tr><td>No users found</td></tr>);
        }

        var hasMore = <div><button class="btn btn-link" onClick={this.loadMore}>Load more users</button></div>;
        return (
            <div>
                <table class="table table-hover forum-user-list">
                    <tbody>
                        {users}
                    </tbody>
                </table>
                {this.state.next ? hasMore : <div></div>}
            </div>
        )
    }
});


var ForumUsers = React.createClass({
    getUrl: function() {
        return this.props.getUrl() + "users/?format=json";
    },

    getInitialState: function() {
        return {list: this.getUrl() + "&type=all"}
    },

    loadUsers: function() {
        //Clearing search bar
        var search = this.refs.search.getDOMNode();
        $(search).val('');

        var selected = this.refs.users.getDOMNode();
        var val = $(selected).find('option:selected').prop('value');

        this.setState({list: this.getUrl()+"&type="+val});
        console.log("Loading users: " + val);
    },

    searchUser: function() {
        // Clearing selected option
        var selected = this.refs.users.getDOMNode();
        $(selected).val([]);

        var search_str = this.refs.search.getDOMNode().value.trim();
        search_str = encodeURIComponent(search_str);

        this.setState({list: this.getUrl()+"&type=search&query="+search_str});
        console.log("Searching for user: " + search_str);
    },

    render: function() {
        if(!this.props.selected) {
            return <div></div>
        }

        return (
            <div id="forum-tags-container">
                <div class="row">
                    <div class="col-lg-3">
                        <div class="input-group">
                            <select ref="users" class="form-control" onChange={this.loadUsers}>
                                <option value="all">All Users</option>
                                <option value="moderators">Moderators</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="input-group">
                            <input ref="search" type="text" class="form-control" placeholder="Search with Username" />
                            <span class="input-group-btn">
                                <button class="btn btn-default" type="button" onClick={this.searchUser}>
                                    <span class="glyphicon glyphicon-search"></span>
                                </button>
                            </span>
                        </div>
                    </div>
                </div>

                <div>
                    <ForumUserList list={this.state.list} />
                </div>
            </div>
        )
    }
});



var ReviewContent = React.createClass({
    getUrl: function() {
        return "/forum/api/content/" + this.props.data.id + "/"
    },

    getInitialState: function() {
        return {deleted: false, approved: false};
    },

    approve: function() {
        // Make GET ajax json call to content/<id>/reset_spam_flags
        // On success mark approved true
        var url = this.getUrl() + "reset_spam_flags/";
        var request = ajax_json_request(url, "GET", {});
        request.success(function(response) {
            this.setState({deleted:false, approved:true});
        }.bind(this));
    },

    remove: function() {
        // Make DELETE ajax json call to content/<id>/
        // On success mark deleted to true
        var url = this.getUrl();
        var request = ajax_json_request(url, "DELETE", {});
        request.success(function(response) {
            this.setState({deleted:true, approved:false});
        }.bind(this));
    },

    dummy: function(_val) {
        //Nothing
        return;
    },

    render: function() {
        if(this.state.deleted) {
            return (
                <tr>
                    <td></td>
                    <td></td>
                    <td>
                        <div class="alert alert-danger alert-dismissable">
                            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                            <strong>Content has been removed !</strong>
                        </div>
                    </td>
                </tr>
            );
        } else if(this.state.approved) {
            return (
                <tr>
                    <td></td>
                    <td></td>
                    <td>
                        <div class="alert alert-success alert-dismissable">
                            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                            <strong>Content has been approved !</strong>
                        </div>
                    </td>
                </tr>
            );
        } else {
            return (
                <tr>
                    <td class="review-content-btn">
                        <button class="btn btn-success btn-sm" onClick={this.approve}>
                            <span class="glyphicon glyphicon-ok"></span>
                        </button>
                    </td>
                    <td class="review-content-btn">
                        <button class="btn btn-danger btn-sm" onClick={this.remove}>
                            <span class="glyphicon glyphicon-trash"></span>
                        </button>
                    </td>
                    <td>
                        <p>
                            {this.props.data.content}
                        </p>
                        <ul class="content-meta-info">
                            <li>by - <UserLink data={this.props.data.author} /> </li>
                            <li><span class="label label-default">{this.props.data.author_badge}</span></li>
                            <li><DynamicDateTime time={this.props.data.created} refreshInterval={500000} /></li>
                            <li><VoteObject onClick={this.dummy} type="thumbs-up" val={this.props.data.upvotes} /></li>
                            <li><VoteObject onClick={this.dummy} type="thumbs-down" val={this.props.data.downvotes}/></li>
                            <li><VoteObject onClick={this.dummy} type="flag" val={this.props.data.spam_count}/></li>
                        </ul>
                    </td>
                </tr>
            );
        }
    }
});


var ForumContentReview = React.createClass({
    mixins: [ListMixin],

    render: function() {
        if(!this.props.selected) {
            return (<div></div>);
        }

        var content = this.state.items.map(function(item) {
            console.log(item);
            return (<ReviewContent key={"review_content_"+item.id} data={item} />);
        }.bind(this));

        var hasMore = (
            <tr>
                <td></td>
                <td></td>
                <td>
                    <button class="btn btn-link" onClick={this.loadMore}>
                        Load more users
                    </button>
                </td>
            </tr>
        );

        return (
            <div>
                <span class="text-mute">Count: {this.state.count}</span>
                <table class="table forum-content-review-container">
                    <tbody>
                        {content}
                        {this.state.next ? hasMore : <tr></tr>}
                    </tbody>
                </table>
            </div>
        )
    }
});

var ForumAdminPanel = React.createClass({
    getInitialState: function() {
        this.loadForum();
        return {loaded: false, selected:[true, false, false, false,]};
    },

    getUrl: function() {
        return "/forum/api/forum/" + this.props.id + "/";
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

    loadContainer: function(index) {
        var state = this.state;
        var links = $(".nav-links > li > a");
        for(var i=0; i<state.selected.length; i++) {
            $(links[i]).removeClass();
            state.selected[i] = false;
        }
        state.selected[index] = true;
        $(links[index]).addClass("nav-link-active");
        this.setState(state);
    },

    loadContainer0: function() {this.loadContainer(0);},
    loadContainer1: function() {this.loadContainer(1);},
    loadContainer2: function() {this.loadContainer(2);},
    loadContainer3: function() {this.loadContainer(3);},

    componentDidMount: function(rootNode) {
        this.loadContainer(0);
    },

    render: function() {
        if(!this.state.loaded) {
            return <LoadingBar />
        }

        return (
            <div class="panel panel-default">
                <div class="panel-heading forum-heading">
                    <h3 class="pull-left">
                        Discussion Forum &nbsp;&nbsp;&nbsp;
                        <span class="forum-text-mute">Admin Panel</span>
                    </h3>
                </div>
                <div class="panel-body">
                    <div class="">
                        <ul class="nav-links nav-links-default">
                            <li><a onClick={this.loadContainer0} class="nav-link-active">Setting</a></li>
                            <li><a onClick={this.loadContainer1}>Tags</a></li>
                            <li><a onClick={this.loadContainer2}>Users</a></li>
                            <li><a onClick={this.loadContainer3}>Content Review</a></li>
                        </ul>
                    </div>

                    <div id="forum-panel-container">
                        <div class="forum-admin-panel-container">
                            <ForumSetting selected={this.state.selected[0]} data={this.state.data} getUrl={this.getUrl} />
                        </div>
                        <div class="forum-admin-panel-container">
                            <ForumTags selected={this.state.selected[1]} tags={this.state.data.tags} getUrl={this.getUrl} />
                        </div>
                        <div class="forum-admin-panel-container">
                            <ForumUsers selected={this.state.selected[2]} data={this.state.tags} getUrl={this.getUrl} />
                        </div>
                        <div class="forum-admin-panel-container">
                            <ForumContentReview selected={this.state.selected[3]} getUrl={this.getUrl} list={this.getUrl()+"review_content/?format=json"} />
                        </div>
                    </div>
                </div>
            </div>
        );
    }
});

React.renderComponent(
    ForumAdminPanel({"id": 1}),
    document.getElementById('admin')
);
