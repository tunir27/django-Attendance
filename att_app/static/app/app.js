var app=angular.module('NewCollegeProject',['ui.router']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.config(function($stateProvider,$urlRouterProvider) {
	$stateProvider
	.state("dashboard", {
        url: "",
        controller: "ctrl_model",
        templateUrl: "student_details"
    })
	$urlRouterProvider.when("","");
});