angular.module("formManager", 
[
    "ui.bootstrap", 
    "ui.select", 
    "formio",
    "ngFormioGrid",
    "ngFormBuilder",
    "ui.tinymce",
    "ngNotify"
])
.config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
})
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
        },
        saveFormDesign: function (form_id, payload) {
            var deferred = $q.defer();
            $http({
                method: 'PUT',
                url: '/api/v1/forms/'+form_id+'/design/',
                data: payload,
                params: {format: 'json'}
            }).then(function (response) {
                deferred.resolve(response.data);
            }).catch(function (err) {
                deferred.reject(err);
            });
            return deferred.promise;
        },
        savePDFOutputSetting: function (form_id, payload) {
            var deferred = $q.defer();
            $http({
                method: 'PUT',
                url: '/api/v1/forms/'+form_id+'/pdf_output_setting/',
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
    ["$scope", "formioComponents", "$timeout", "formManagerService", "ngNotify",
        function($scope, formioComponents, $timeout, formManagerService, ngNotify){
            $scope.form = null;
            $scope.form_schema = null;
            $scope.form_id = location.pathname.split('/')[1];
            $scope.host = location.origin;
            $scope.share_url = $scope.host+'/'+$scope.form_id+'/share/';
            $scope.form_details_url = $scope.host+'/api/v1/forms/'+$scope.form_id+'/details'

            // Generate documents
            $scope.generate_pdf = false;
            $scope.pdf_output_template = null;
            $scope.tinymceOptions = TINYMCE_OPTIONS;

            // Get form on init
            $scope.getForm = function() {
                return formManagerService.getForm($scope.form_id).then(function (res) {
                    $scope.form = res;
                    $scope.form_schema = JSON.parse(res.schema);
                    $scope.generate_pdf = res.generate_pdf;
                    $scope.pdf_output_template = res.pdf_output_template;
                }).catch(function (err) {
                    ngNotify.set(err.data, {sticky: true,type: 'error'});
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
                    ngNotify.set('Form saved');
                }).catch(function (err) {
                    console.log(err);
                    ngNotify.set(err.data, {sticky: true,type: 'error'});
                });
            }

            // Update form design
            $scope.updateFormDesign = function() {
                var payload = {
                    schema: JSON.stringify($scope.form_schema)
                }
                return formManagerService.saveFormDesign($scope.form_id, payload).then(function (res) {
                    ngNotify.set('Form design updated');
                }).catch(function (err) {
                    console.log(err);
                    ngNotify.set(err.data, {sticky: true,type: 'error'});
                });
            }

            // Save PDF output settings
            $scope.updatePDFOutputSettings = function() {
                var payload = {
                    generate_pdf: $scope.generate_pdf,
                    pdf_output_template: $scope.pdf_output_template
                }
                return formManagerService.savePDFOutputSetting($scope.form_id, payload).then(function (res) {
                    ngNotify.set('PDF Output preference updated');
                }).catch(function (err) {
                    ngNotify.set(err.data, {sticky: true,type: 'error'});
                });
            }
        }
    ]
);