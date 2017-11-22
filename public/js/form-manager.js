angular.module("formManager", 
[
    "ui.bootstrap", 
    "ui.select", 
    "formio",
    "ngFormioGrid"
])
.factory('formManagerService', function ($http, $q, $rootScope) {
    return {
        getForm: function (form_id) {
            var deferred = $q.defer();
            $http({
                method: 'GET',
                url: '/api/v1/forms/'+form_id,
                params: {format: 'json'}
            }).then(function (response) {
                deferred.resolve(response.data);
            }).catch(function (err) {
                deferred.reject(err);
            });
            return deferred.promise;
        },
        saveFormDetails: function (form_id, payload) {
            var deferred = $q.defer();
            $http({
                method: 'PUT',
                url: '/api/v1/forms/'+form_id+'/',
                data: payload,
                params: {format: 'json'}
            }).then(function (response) {
                deferred.resolve(response.data);
            }).catch(function (err) {
                deferred.reject(err);
            });
            return deferred.promise;
        }
    }
})
.controller('formManagerController', 
    ["$scope", "formioComponents", "$timeout", "formManagerService", 
        function($scope, formioComponents, $timeout, formManagerService){
            $scope.form = null;
            $scope.form_id = location.pathname.split('/')[2];

            // Get form on init
            $scope.getForm = function() {
                return formManagerService.getForm($scope.form_id).then(function (res) {
                    $scope.form = res;
                }).catch(function (err) {
                    console.log(err);
                });
            }
            
            // Save form details
            $scope.saveFormDetails = function() {
                var payload = {
                    title: $scope.form.title,
                    description: $scope.form.description
                };
                return formManagerService.saveFormDetails($scope.form_id, payload).then(function (res) {
                    $scope.form = res;
                }).catch(function (err) {
                    console.log(err);
                });
            }
        }
    ]
);