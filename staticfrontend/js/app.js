'use strict';

/* App Module */

var wineApp = angular.module('wineApp', [
  'ngRoute',
  'wineControllers',
]);

wineApp.config(['$routeProvider', '$httpProvider',
  function($routeProvider, $httpProvider){
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $routeProvider.
      when('/wines', {
        templateUrl: 'partials/wine-list.html',
        controller: 'WineListCtrl'
      }).
      when('/wines/new', {
        templateUrl: 'partials/wine-new.html',
        controller: 'WineDetailCtrl'
      }).
      when('/wines/:wineId', {
        templateUrl: 'partials/wine-detail.html',
        controller: 'WineDetailCtrl'
      }).
      otherwise({
        redirectTo: '/wines'
      });
  }]);
