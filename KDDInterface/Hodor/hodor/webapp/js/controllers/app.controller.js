var app = angular.module('AF', ['ngResource','angularModalService','ui.router','nvd3ChartDirectives']);


app.controller('MainCtrl', function ($scope, $state) {
	$state.go('dashboard');
});

app.config(function ($stateProvider) {
	$stateProvider
		.state('dashboard', {
			url: '/dashboard',
			views: {
				'content@': {
					templateUrl: '/html/dashboard.html',
					controller: 'dashboardCtrl'
				}
			}
		})
		.state('viewresults', {
			url: '/viewresults',
			views: {
				'content@': {
					templateUrl: '/html/viewresults.html',
					controller: 'viewresultsCtrl'
				}
			}
		});
	});