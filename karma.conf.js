// Karma configuration
// Generated on Fri Oct 17 2014 14:45:10 GMT+0300 (EAT)

module.exports = function(config) {
  config.set({

    // base path, that will be used to resolve files and exclude
    basePath: '',


    // frameworks to use
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      'questionnaire/static/js/lib/angular.min.js',
      'spec/lib/angular-mocks.js',
      'questionnaire/static/js/lib/*.js',
      'questionnaire/static/js/create_skip_rule.js',
      'questionnaire/static/js/ng-client/**/*.js',
      'questionnaire/static/bootstrap-datetimepicker/bootstrapdatepicker.js',
      'spec/*.js'
    ],


    // list of files to exclude
    exclude: [
        'questionnaire/static/js/export-section.js',
        'questionnaire/static/js/application.js'
    ],


    // test results reporter to use
    // possible values: 'dots', 'progress', 'junit', 'growl', 'coverage'
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // Start these browsers, currently available:
    // - Chrome
    // - ChromeCanary
    // - Firefox
    // - Opera (has to be installed with `npm install karma-opera-launcher`)
    // - Safari (only Mac; has to be installed with `npm install karma-safari-launcher`)
    // - PhantomJS
    // - IE (only Windows; has to be installed with `npm install karma-ie-launcher`)
    browsers: ['PhantomJS'],


    // If browser does not capture in given timeout [ms], kill it
    captureTimeout: 60000,


    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: true
  });
};
