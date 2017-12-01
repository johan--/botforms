angular.module("shareForm", 
[
    "ui.bootstrap", 
    "ui.select", 
    "formio", 
    "ngNotify"
])
.config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
})
.factory('shareFormService', function ($http, $q, $rootScope) {
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
        saveSubmission: function (payload) {
            var deferred = $q.defer();
            $http({
                method: 'POST',
                url: '/api/v1/submissions/',
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
.controller('shareFormController', 
    ["$scope", "formioComponents", "$timeout", "ngNotify", "shareFormService", 
        function($scope, formioComponents, $timeout, ngNotify, shareFormService){
            $scope.form = {};
            $scope.schema = {};
            $scope.form_id = location.pathname.split('/')[1];

            // Capture reference id if any
            $scope.reference = getParameterByName('reference');

            // Get route parameters
            function getParameterByName(name, url) {
                if (!url) url = window.location.href;
                name = name.replace(/[\[\]]/g, "\\$&");
                var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                    results = regex.exec(url);
                if (!results) return null;
                if (!results[2]) return '';
                return decodeURIComponent(results[2].replace(/\+/g, " "));
            }            

            // Get form from the database
            $scope.getForm = function() {
                return shareFormService.getForm($scope.form_id).then(function (res) {
                    $scope.form = res;
                    $scope.schema = JSON.parse(res.schema);
                }).catch(function (err) {
                    console.log(err);
                });
            }

            // Save form
            try {
                $scope.$on('formSubmission', function (event, submission) {
                    event.stopPropagation();
                    var payload = {
                        form: $scope.form_id,
                        data: JSON.stringify(submission),
                        reference: $scope.reference
                    };
                    shareFormService.saveSubmission(payload).then(function (res) {
                        window.location.href = '/success';
                    }).catch(function (err) {
                        console.log(err);
                        ngNotify.set(err.data, {sticky: true,type: 'error'});
                    });
                });
            } catch (err) {
                console.log(err);
                ngNotify.set(err, {sticky: true,type: 'error'});
            }
        }
    ]
);