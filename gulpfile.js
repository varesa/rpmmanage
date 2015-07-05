/* gulpfile.js */
 
// Load some modules which are installed through NPM.
var gulp = require('gulp');
var browserify = require('browserify');  // Bundles JS.
var reactify = require('reactify');  // Transforms React JSX to JS.
var source = require('vinyl-source-stream');

// Our JS task. It will Browserify our code and compile React JSX files.
gulp.task('js', function() {
  browserify("./client_js/main.js")
    .transform(reactify)
    .bundle()
    .pipe(source('bundle.js'))
    .pipe(gulp.dest('./static/js/'));
});
 
// Rerun tasks whenever a file changes.
gulp.task('watch', function() {
  gulp.watch("./client_js/*", ['js']);
});
 
// The default task (called when we run `gulp` from cli)
gulp.task('default', ['watch', 'js']);