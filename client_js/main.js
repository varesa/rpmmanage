var React = require('react');
var Flux = require('flux');
$ = jQuery = require('jquery');



var ReactProjectList = require('./components/ReactProjectList');

var Dispatcher = require('./Dispatcher');
dispatcher = new Dispatcher();

var ProjectStore = require('./ProjectStore');
projectStore = new ProjectStore();

$(document).ready(function() {
    React.render(<ReactProjectList />, $("#main")[0]);
});