angular.module("formBuilder", 
[
    "ui.bootstrap", 
    "ui.select", 
    "formio", 
    "ngFormBuilder",
    "ngNotify"
])
.factory('formBuilderService', function ($http, $q, $rootScope) {
    return {
        createForm: function (payload) {
            var deferred = $q.defer();
            $http({
                method: 'POST',
                url: '/api/v1/forms/',
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
.config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
})
.controller('formBuilderController', 
    ["$scope", "formioComponents", "$timeout", "formBuilderService", "ngNotify", 
        function($scope, formioComponents, $timeout, formBuilderService, ngNotify){
            $scope.form = {
                title: null,
                description: null,
                schema: {
                    components: [{}],
                    display: 'form',
                    _id: 1
                }
            };
            
            // Save form
            $scope.saveFormBtn = function() {
                var payload = {
                    title: $scope.form.title,
                    description: $scope.form.description,
                    schema: JSON.stringify($scope.form.schema)
                }
                return formBuilderService.createForm(payload).then(function (res) {
                    window.location.href = '/'
                }).catch(function (err) {
                    ngNotify.set(err.data, {sticky: true,type: 'error'});
                });
            }
            
        }
    ]
);