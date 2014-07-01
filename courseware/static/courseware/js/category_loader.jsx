/** @jsx React.DOM */

var CategoryLoader = React.createClass({
    getInitialState: function() {
        return {
            loaded: false,
            parent_categories: undefined,
            categories: undefined,
            category_loaded: false,
            defaultCategory: undefined,
            defaultParentCategory: undefined,
        };
    },

    componentDidMount: function() {
        if(!this.state.loaded) {
            console.log("getting defaultParentCategory")
            this.setState({
                defaultCategory: this.props.defaultCategory,
            });
            if (this.state.defaultCategory) {
                url = "/courseware/api/category/" + this.state.defaultCategory + "/?format=json";
                request = ajax_json_request(url, "GET", {});
                request.done(function(response) {
                    response = jQuery.parseJSON(response);
                    this.setState({defaultParentCategory: response.parent});
                }.bind(this));
            }
            this.loadParentCategories();
        }
    },

    loadParentCategories: function() {
        url = "/courseware/api/parent_category/?format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            this.setState({parent_categories: response.results, loaded: true});
            this.loadCategories(undefined, this.state.defaultParentCategory);
        }.bind(this));
    },

    loadCategories: function(selectObj, parentCategory) {
        oldState = this.state;
        oldState.category_loaded=false;
        this.setState(oldState);
        console.log(parentCategory);
        if (parentCategory) {
            pcid = parentCategory;
        } else {
            console.log(this.refs.parent_category.getDOMNode());
            pcid = this.refs.parent_category.getDOMNode().value.trim();
        }
        console.log(pcid);
        url = "/courseware/api/category/?parent="+ pcid + "&format=json";
        request = ajax_json_request(url, "GET", {});
        request.done(function(response) {
            response = jQuery.parseJSON(response);
            oldState = this.state;
            oldState.categories = response.results;
            oldState.category_loaded=true;
            this.setState(oldState);
            this.handleCategoryChange();
        }.bind(this));
    },

    handleCategoryChange: function() {
        category = this.refs.category.getDOMNode().value.trim();
        this.props.callback(category);
    },

    render: function() {
        if (!this.state.loaded){
            return (
                <LoadingBar />
            );
        }
        else {
            console.log(this.state);
            var parent_category = this.state.parent_categories.map(
                function (category) {
                    if (category.id != this.state.defaultParentCategory){
                        return <option value={category.id}>{category.title} </option>;
                    } else {
                        return <option value={category.id} selected="selected">{category.title} </option>;
                    }
                }.bind(this));
            if (this.state.category_loaded) {
                var category = this.state.categories.map(function (cat) {
                    if (cat.id == this.defaultCategory) {
                        return <option value={cat.id} selected="selected">{cat.title}</option>;
                    } else {
                        return <option value={cat.id}>{cat.title}</option>;
                    }
                });
                var category_select =
                    <select class="form-control" onChange={this.handleCategoryChange} ref="category">
                        {category}
                    </select>;
            }
            else {
                category_select =
                    <select class="form-control" ref="category" disabled>
                    </select>;
            }
            return (
                <div>
                    <div class="form-group">
                        <label class="control-label col-md-3 col-md-offset-0">Parent Category</label>
                        <div class="col-md-7 col-md-offset-1">
                            <select onChange={this.loadCategories} ref="parent_category" class="form-control">
                                {parent_category}
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="control-label col-md-2 col-md-offset-1">Category</label>
                        <div class="col-md-7 col-md-offset-1">
                            {category_select}
                        </div>
                    </div>
                </div>
            )
        }
    }
});