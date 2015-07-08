var React = require('react');
var Flux = require('flux');
$ = jQuery = require('jquery');



var ReactApp = require('./components/ReactApp');

var Dispatcher = require('./Dispatcher');
dispatcher = new Dispatcher();

var ProjectStore = require('./stores/ReactProjectStore');
projectStore = new ProjectStore();

var TargetStore = require('./stores/TargetStore');
targetStore = new TargetStore();

$(document).ready(function() {
    React.render(<ReactApp />, $("#main")[0]);
});