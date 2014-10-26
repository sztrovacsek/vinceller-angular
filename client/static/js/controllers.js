'use strict';

/* Controllers */

var wineControllers = angular.module('wineControllers', []);

wineControllers.controller('WineListCtrl', ['$scope', '$http',
  function($scope, $http) {
    $http.get('/api/wine_list').success(function(data) {
      $scope.wines = data;
    });

    $scope.orderProp = 'age';
  }]);

wineControllers.controller('WineDetailCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {
    $http.get('/api/wine_detail/' + $routeParams.phoneId).success(function(data) {
      $scope.wine = data;
    });
  }]);
