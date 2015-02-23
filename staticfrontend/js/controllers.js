'use strict';

/* Controllers */

var wineControllers = angular.module('wineControllers', []);

wineControllers.filter('presence', function() {
  return function(input, avail, tasted, wished){
    input = input || [];
    var output = [];
    for (var i =0; i < input.length; i++){
      var wine = input[i];
      if (avail && wine.status == "available") { output.push(wine); }
      if (tasted && wine.status =="tasted") { output.push(wine); }
      if (wished && wine.status == "wished") { output.push(wine); }
    }
    return output;
  };
});

wineControllers.controller('WineListCtrl', ['$scope', '$http', 'presenceFilter',
  function($scope, $http, presenceFilter) {
    $scope.orderProp = '-id';
    $scope.check_avail = true;

    $http.get('/api/wine_list').success(function(data) {
      $scope.wines = data;
      $scope.filteredWines = presenceFilter($scope.wines, $scope.check_avail, $scope.check_tasted, $scope.check_wished);
    });

    $http.get('/api/user_info').success(function(data) {
      $scope.username = data.username;
      $scope.user_logged_in = data.logged_in;
    });
  }]);

wineControllers.controller('WineDetailCtrl', ['$scope', '$routeParams', '$http',
  function($scope, $routeParams, $http) {
    $scope.edit = false;

    $http.get('/api/wine_detail/' + $routeParams.wineId).success(function(data) {
      $scope.wine = data;
      console.log($scope.wine);
    });

    $scope.startEdit = function(){
      console.log("Enable editing");
      $scope.edit = true;
    }

    $scope.saveEdit = function(){
      console.log("Saving editing");
      $scope.edit = false;
      console.log($scope.wine);
      // post the data to the server
      $.ajax({
        url: "/api/wine_update",
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: $scope.wine,
        type: "POST",
        dataType: "JSON",
        success: function(json){
          console.log("Post succeeded");
        }
        /*
        error: function(xhr, status, errorThrown){
          console.log("Post error");
        }
        */
      });
    }

    $scope.cancelEdit = function(){
      console.log("Cancelling editing");
      $scope.edit = false;
    }

  }]);
