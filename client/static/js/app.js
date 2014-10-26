'use strict';

/* App Module */

var wineApp = angular.module('wineApp', [
  'ngRoute',
  'wineControllers'
]);

wineApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/wines', {
        templateUrl: 'partials/wine-list.html',
        controller: 'WineListCtrl'
      }).
      when('/wines/:phoneId', {
        templateUrl: 'partials/wine-detail.html',
        controller: 'WineDetailCtrl'
      }).
      otherwise({
        redirectTo: '/wines'
      });
  }]);
