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
    $http.get('/api/wine_detail/' + $routeParams.wineId).success(function(data) {
      $scope.wine = data;
    });

    $scope.edit = false;

    $scope.startEdit = function(){
      console.log("Enable editing");
      $scope.edit = true;
    }

    $scope.saveEdit = function(){
      console.log("Saving editing");
      $scope.edit = false;
      console.log($scope.wine);
    }

    $scope.cancelEdit = function(){
      console.log("Cancelling editing");
      $scope.edit = false;
    }

  }]);
