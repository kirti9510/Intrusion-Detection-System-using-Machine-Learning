var app = angular.module('AF');

app.controller('viewresultsCtrl', function ($scope, $http) {
	$scope.packets = null;
	$scope.pack = null;
	$http.get('/api/get_data').then(function(response){
		$scope.packets = response.data.result;
	});	
});