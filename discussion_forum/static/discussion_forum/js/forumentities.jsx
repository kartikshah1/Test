/** @jsx React.DOM */

var Reply = React.createClass({
    mixins: [ContentUpdateMixin],

    getInitialState: function() {
        new_state = {
            "data": this.props.data
        };

        return new_state;
    },

    render: function() {
        if(this.state.deleted) {
            return (
                <div class="alert alert-info alert-dismissable forum-delete-info">
                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                    <strong>Reply has been removed !</strong>
                </div>
            )
        }
        return (
            <Content current_user={this.props.current_user} type="reply" data={this.state.data} callback={this.updateContentData} remove={this.remove} />
        )
    }
});


var ReplyList = React.createClass({
    mixins: [ListMixin],

    render: function() {
        var replyNodes = this.state.items.map(function (reply) {
            return <tr><td><Reply current_user={this.props.current_user} data={reply} callback={this.props.callback} /></td></tr>;
        }.bind(this));
        var hasMore = <tr><td class="reply"><button class="btn btn-link" onClick={this.loadMore}>Load more replies</button></td></tr>;
        return (
            <div class="reply-list">
                <table class="table">
                    {replyNodes}
                    {this.state.next ? hasMore : <tr></tr>}
                    <tr>
                        <td class="reply">
                            <ContentForm type="Reply" submit={this.submitContentForm} callback={this.props.callback} />
                        </td>
                    </tr>
                </table>
            </div>
        )
    }
});


var Comment = React.createClass({
    mixins: [ContentUpdateMixin],

    getUrl: function(_id) {
        return "/forum/api/comment/" + _id + "/";
    },

    getInitialState: function() {
        _url = this.getUrl(this.props.data.id);
        new_state = {
            "replies": _url + "replies/?format=json",
            "add_reply": _url + "add_reply/?format=json",
            "data": this.props.data
        };

        return new_state;
    },

    render: function() {
        if(this.state.deleted) {
            return (
                <div class="alert alert-info alert-dismissable forum-delete-info">
                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                    <strong>Comment has been removed !</strong>
                </div>
            )
        }
        return (
            <div>
                <Content current_user={this.props.current_user} type="comment" data={this.state.data} callback={this.updateContentData} remove={this.remove} />
                <div>
                    <ReplyList current_user={this.props.current_user} list={this.state.replies} add={this.state.add_reply} callback={this.updateChildrenCount} />
                </div>
            </div>
        )
    }
});


var CommentList = React.createClass({
    mixins: [ListMixin],

    render: function() {
        var commentNodes = this.state.items.map(function (comment) {
            return <tr><td><Comment key={"comment_"+comment.id} current_user={this.props.current_user} data={comment} callback={this.props.callback} /></td></tr>;
        }.bind(this));
        if(!commentNodes) {
            commentNodes = <LoadingBar />;
        }
        var hasMore = <tr><td class="comment"><button class="btn btn-link" onClick={this.loadMore}>Load more comments</button></td></tr>;
        return (
            <table class="table comment-list">
                {commentNodes}
                {this.state.next ? hasMore : <tr></tr>}
                <tr>
                    <td class="comment">
                        <div>
                            <ContentForm type="Comment" submit={this.submitContentForm} callback={this.props.callback} />
                        </div>
                    </td>
                </tr>
            </table>
        );
    }
});


var Thread = React.createClass({
    mixins: [ContentUpdateMixin],

    getUrl: function(_id) {
        return "/forum/api/thread/" + _id + "/";
    },

    getInitialState: function() {
        _url = this.getUrl(this.props.data.id);
        new_state = {
            "comments": _url + "comments/?format=json",
            "add_comment": _url + "add_comment/?format=json",
            "loaded": false,
            "data": this.props.data
        };

        return new_state;
    },

    loadComments: function() {
        var state = this.state;
        if(state.loaded) {
            return;
        } else {
            state.loaded = true;
            this.setState(state);
        }
    },

    render: function() {
        if(this.state.deleted) {
            return (
                <div class="alert alert-info alert-dismissable forum-delete-info">
                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
                    <strong>Thread has been removed !</strong>
                </div>
            )
        }

        var pinned = '';
        if(this.state.data.pinned) {
            pinned = <li><span class="glyphicon glyphicon-pushpin"></span></li>;
        }

        var comment_list = '';
        if(this.state.loaded) {
            comment_list = <CommentList current_user={this.props.current_user}  list={this.state.comments} add={this.state.add_comment} callback={this.updateChildrenCount} />;
        } else {
            <LoadingBar />
        }
        return (
            <div class="panel panel-default">
                <div class="panel-heading">
                    <table class="thread-heading">
                        <tr>
                            <td>
                                <h4 class="panel-title">
                                    <a onClick={this.loadComments} class="accordion-toggle" data-toggle="collapse" data-parent="#accordion" href={"#thread" + this.props.data.id}>
                                        {this.props.data.title}
                                    </a><br/>
                                    <ul class="content-meta-info thread-meta-info">
                                        {pinned}
                                        <li><DynamicDateTime time={this.props.data.created} refreshInterval={20000} /></li>
                                        <li>posted by - <UserLink data={this.props.data.author} /></li>
                                        <li><span class="label label-default">{this.props.data.author_badge}</span></li>
                                        <li><ThreadSubscription thread_id={this.props.data.id} subscribed={this.props.data.subscribed} /></li>
                                    </ul>
                                </h4>
                            </td>
                            <td class="thread-vote-icon"><span class="glyphicon glyphicon-star"> {' ' + this.state.data.popularity}</span></td>
                            <td class="thread-vote-icon"><span class="glyphicon glyphicon-eye-open"> {' ' + this.state.data.hit_count}</span></td>
                            <td class="thread-vote-icon"><span class="glyphicon glyphicon-comment"> {' ' + this.state.data.children_count}</span></td>
                        </tr>
                    </table>
                </div>
                <div id={"thread" + this.props.data.id} class="panel-collapse collapse">
                    <div class="panel-body thread-panel-body">
                        <ThreadTagList thread_id={this.props.data.id} thread_tags={this.props.data.tags} forum_tags={this.props.forum_tags} />
                        <Content current_user={this.props.current_user} type="thread" data={this.state.data} callback={this.updateContentData} remove={this.remove}/>
                        {comment_list}
                    </div>
                </div>
            </div>
        );
    }
});


var ThreadList = React.createClass({
    mixins: [ListMixin],

    dummy: function(index) {
        return;
    },

    render: function() {
        var threadNodes = this.state.items.map(function (thread) {
            return <Thread current_user={this.props.current_user} data={thread} forum_tags={this.props.forum_tags} callback={this.dummy} />;
        }.bind(this));
        var more = '';
        if(this.state.next != null) {
            more = <div><button class="btn btn-link" onClick={this.loadMore}>Load more threads</button></div>;
        }
        return (
            <div class="thread-list">
                <SortOrders order={this.updateSortOrder} />
                <ThreadForm add={this.props.add} add_tag={this.props.add_tag} tags={this.props.forum_tags} submit={this.submitContentForm} callback={this.dummy} />
                <hr/>

                <div class="panel-group" id="accordion">
                    {threadNodes}
                </div>
                {more}
            </div>
        )
    }
});
