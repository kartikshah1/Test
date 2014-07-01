/*
    Mixin to store, access and modify the saved status
    of components that are used to edit something saved on the sever.
    -> Check and change the status directly using 'checkFor' and
        'changeTo', or using the auxiliary functions.
    -> Use 'savedIf' to set the status
        subject to a conditon.
    -> To trigger callbacks etc., define a function
        onSavedStatusChange in your component and handle callbacks
        there based on the changed state. It will be called every
        time the status is changed.
    -> Set the initial savedStatus in componentWillMount
    -> Use selectBySavedStatus to pick one of three things based on satus
    -> As far as possible, avoid setting this.state.savedStatus manually
*/

var SavedStatusMixin = {
    componentWillMount: function() {
        this.setState({savedStatus: 'saved'});
    },

    checkFor: function(status) {
        return this.state.savedStatus == status;
    },

    changeTo: function(status) {
        this.setState({savedStatus: status}, this.onSavedStatusUpdate);
    },

    savedIf: function (check) {
        this.changeTo(check ? 'saved' : 'unsaved');
    },

    selectBySavedStatus: function(options){
        return options[this.state.savedStatus];
    },

    isSaved: function() {
        return this.checkFor('saved');
    },

    isUnsaved: function() {
        return this.checkFor('unsaved');
    },

    isSaving: function() {
        return this.checkFor('saving');
    },

    toSaved: function() {
        this.changeTo('saved');
    },

    toSaving: function() {
        this.changeTo('saving');
    },

    toUnsaved: function() {
        this.changeTo('unsaved');
    }
};


/*
    Depends On : SavedStatusMixin

    This mixin provides a style object that can be
    applied to a div etc., to change its background-color
    based on the savedStatus of the component.

    To disable, sef noTransition to true
*/
var BackgroundTransitionMixin = {
    getBackgroundTransitionStyle: function(colors, noTransition, duration){
        if (noTransition) return {};
        if (!colors) colors = {};
        if (!duration) duration = 1000;

        transition = 'background-color ' + duration + 'ms linear';
        style = {
            WebkitTransition: transition,
            MozTransition: transition,
            OTransition: transition,
            MsTransition: transition,
            'transition': transition
        }

        if (!colors.unsaved) colors.unsaved = '#e4f2ff';
        if (!colors.saved) colors.saved = '#ffffff';
        if (!colors.saving) colors.saving = '#f0f8ff';

        style.backgroundColor = this.selectBySavedStatus(colors);

        return style;
    }
}

var StyleTransitionMixin = {
    getStyleTransition: function(property, duration){
        if (!duration) duration = 1000;
        transition = property + ' ' + duration + 'ms linear';
        return {
            WebkitTransition: transition,
            MozTransition: transition,
            OTransition: transition,
            MsTransition: transition,
            'transition': transition
        };
    }
}
