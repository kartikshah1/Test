/** @jsx React.DOM */

var converter = new Showdown.converter();

var Paginator = React.createClass({
    setPage: function(event) {
        element_a = $(event.target);
        element_li = element_a.parent();
        pos = element_li.parent().index();
        if (this.props.totalPages <= this.props.maxPages) {
            this.props.callback(this.state.start + pos);
        }
        else {
            if (pos == 0) {
                start_ = (this.state.start == 1) ? 1 : (this.state.start - 1);
                end_ = start_ + this.props.maxPages - 1;
                this.setState({start: start_, end: end_});
            }
            else if (pos == (this.props.maxPages + 1)) {
                end_ = (this.state.end == this.props.totalPages) ? this.state.end : (this.state.end + 1);
                start_ = end_ - this.props.maxPages + 1;
                this.setState({start: start_, end: end_});
            }
            else {
                this.props.callback(this.state.start + pos - 1);
            }
        }
    },
    getInitialState: function() {
        return {
            start: 0,
            end: 0
        };
    },
    componentWillMount: function() {
        start_ = 1;
        end_ = this.props.totalPages > this.props.maxPages ?
                this.props.maxPages :
                this.props.totalPages;
        this.setState({start: start_, end: end_});
    },
    render: function() {
        // parameters:
        //   maxPages
        //   totalPages
        //   callback function
        var prev = <div class="col-md-1 no-padding"><a href="javascript:void(0);" class="thumbnail" ref="prev" onClick={this.setPage}><img class="navigators" src="/static/elearning_academy/img/blackleft.jpg" alt="..." /></a></div>;
        var next = <div class="col-md-1 no-padding"><a href="javascript:void(0);" class="thumbnail" ref="next" onClick={this.setPage}><img class="navigators" src="/static/elearning_academy/img/blackright.jpg" alt="..." /></a></div>;
        pages = [];
        for (var i = this.state.start; i <= this.state.end; i++) {
            element = <div>{this.props.category[i-1]}</div>;
            pages[i-1] = element;
        }
        /*TODO: Hard Coded, needs to be dynamics
         */
        if(this.state.end<=10){
            prev = "";
            next = "";
        }
        return (
            <div>
                <h2 style={{'margin-top': '0px'}}> {this.props.heading} </h2>
                <p class='text-info'> {this.props.description} </p>
                {prev}
                {pages}
                {next}
            </div>
        );
    }
});

var MinorList = React.createClass({
    mixins: [LoadMixin],

    getUrl: function() {
        var url = '';
        if(this.props.coursepage=='2') {
            url = '/courseware/api/' + this.props.suburl + '?' + this.props.subsuburl + this.props.id + '&format=json';
        }
        else {
            url = '/courseware/api/' + this.props.suburl + this.props.id + this.props.subsuburl + '?format=json';
        }
        return url;
    },

    getInitialState: function() {
        return {
            loaded: false,
            data: undefined
        };
    },

    render: function() {
        if (this.state.loaded) {
            var results = this.state.data;
            if (this.props.coursepage=='2') {
                results = results.results;
            }
            var categories = results.map(function (category) {

                path = "/media/" + category.image;
                if (this.props.subhpath == "#" ) {
                    hrefpath = "#";
                }
                else {
                    hrefpath = "/courseware" + this.props.subhpath + "/" + category.id;
                }
                return <div class="col-md-3">
                            <div class="thumbnail sliders">

                                <img class="mimage" src={path} alt="Not Available" />
                                <a class="caption smallheading" href={hrefpath}><h5>{category.title}</h5>
                                </a>
                            </div>
                        </div>
            }.bind(this));
            return (
                <Paginator
                    key={this.props.id}
                    category={categories}
                    totalPages={categories.length}
                    maxPages={3}
                    callback={this.setPage}
                />
            );
        }
        else {
            return (
                <LoadingBar />
            );
        }
    }
});

var CourseList = React.createClass({
    mixins: [LoadMixin],

    getUrl: function() {
        var url = '';
        url = '/courseware/api/all_courses' + '?' + 'format=json';
        return url;
    },

    getInitialState: function() {
        return {
            loaded: false,
            data: undefined
        };
    },

    render: function() {
        if (this.state.loaded) {
            var results = this.state.data;
            if(results.count==0){
                return (<div class="col-md-3">
                No courses</div>);
            }
            if (this.props.coursepage=='2') {
                results = results.results;
            }
            var courses = results.map(function (course) {

                path = "/media/" + course.image;
                if (this.props.subhpath == "#" ) {
                    hrefpath = "#";
                }
                else {
                    hrefpath = "/courseware" + this.props.subhpath + "/" + course.id;
                }
                return <div class="col-md-3">
                            <div class="thumbnail sliders">

                                <img class="mimage" src={path} alt="Not Available" />
                                <a class="caption smallheading" href={hrefpath}><h5>{course.title}</h5>
                                </a>
                            </div>
                        </div>
            }.bind(this));
            return (
                <Paginator
                    key={this.props.id}
                    category={courses}
                    totalPages={courses.length}
                    maxPages={3}
                    callback={this.setPage}
                    heading={this.props.heading}
                    description={this.props.description}
                >
                </Paginator>
            );
        }
        else {
            return (
                <LoadingBar />
            );
        }
    }
});

/*var MajorList = React.createClass({
    mixins: [LoadMixin],

    getUrl: function() {
        url = '/courseware/api/' + this.props.myurl + "&format=json";
        return url;
    },

    getInitialState: function() {
        return {
            loaded: false,
            data: undefined
        };
    },

    render: function() {
        var categories = '';
        if (this.state.loaded) {
            categories = this.state.data.results.map(function (category) {
                var hrefpath = "/courseware" + this.props.hrefpath + "/" + category.id;
                var minorlist = '';
                if (this.props.coursepage=='2') {
                    minorlist = (
                        <div class="col-md-9">
                            <MinorList
                                key={category.id}
                                suburl={this.props.suburl}
                                subsuburl={this.props.subsuburl}
                                subhpath={this.props.subhpath}
                                coursepage = {this.props.coursepage}
                                id={category.id} />
                        </div>
                    );
                }
                return  <div class="row listrow">
                            <a class="col-md-3 largeheading" href={hrefpath}>
                                <h3>{category.title}</h3>
                            </a>
                            {minorlist}
                        </div>;
            }.bind(this));
        }
        else {
            categories = <LoadingBar />;
        }
        return (
            <div>
                <h2 style={{'margin-top': '0px'}}> {this.props.heading} </h2>
                <p class='text-info'> {this.props.description} </p>
                <br/>
                {categories}
            </div>
        );
    }
});*/
