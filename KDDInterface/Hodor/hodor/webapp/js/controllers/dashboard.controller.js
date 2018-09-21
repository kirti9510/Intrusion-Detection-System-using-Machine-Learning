var app = angular.module('AF');

app.controller('dashboardCtrl', function ($scope, $http, $timeout, $location) {
	$scope.predict = null;
	$scope.learn = null;

	$scope.check_status = function() {
		$http.get('/api/pcap_is_running').then(function(response){
			$scope.predict = response.predict;
			$scope.learn = response.learn;
			$timeout($scope.check_status, 2000);
		});
	}

	$scope.startTrain = function() {
		$http.get('/api/pcap_learn/True').then(function(response){
			$scope.learn = true;
			$scope.predict = false;
		});
		$http.get('/api/pcap_learn/False').then(function(response){
			$timeout($scope.check_status, 2000);
		});
		
	}

	

	$scope.startPredict = function() {
		$http.get('/api/pcap_predict/True').then(function(response){
			$scope.predict = true;
			$scope.learn = false;
		});	
	}

	$scope.viewResults = function() {
		$location.path("/viewresults");
	}

});