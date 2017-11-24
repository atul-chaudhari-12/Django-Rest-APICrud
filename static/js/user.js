/**
 * @author atul
 */

var userapp = angular.module('userapp',['angularModalService']);

userapp.config(function($interpolateProvider) {
		$interpolateProvider.startSymbol('{[{');
		$interpolateProvider.endSymbol('}]}');
	});

userapp.directive('fileModel', ['$parse', function ($parse) { //directive for uploading file
            return {
               restrict: 'A',
               link: function(scope, element, attrs) {
                  var model = $parse(attrs.fileModel);
                  var modelSetter = model.assign;
                  
                  element.bind('change', function(){
                     scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                     });
                  });
               }
            };
         }]);
      
 userapp.service('fileUpload',['$http', function($http){ //serview to call backed api to store file
    this.uploadFileToUrl = function(file, uploadUrl){
       var fd = new FormData();
       fd.append('file', file);
    
       $http.post(uploadUrl, fd, {
          transformRequest: angular.identity,
          headers: {'Content-Type': undefined}
       }).then(function(data){
       		a1 = angular.element($("#editprofile")).scope();
       		a1.customObj.user_profile_pic1 = "/static/"+data.data.split("/static/")[1];
       		sessionStorage.setItem('change_profile_pic',data.data);
       });
    };
 }]);

userapp.controller('UserController',['$scope','$http','$compile','ModalService','fileUpload',
	function UserController($scope,$http,$compile,ModalService,fileUpload){
	$scope.first_variable = "author_atul";
	$scope.customObj = {};

	//Log in depending on type
	$scope.login=function(type){
		
		if (type=='staff'){
			email = angular.element($("#email1")).val()
			password = angular.element($("#exampleInputPassword1")).val()
		}else if(type=='student'){
			email = angular.element($("#email2")).val()
			password = angular.element($("#exampleInputPassword2")).val()
		}else{
			email = angular.element($("#email3")).val()
			password = angular.element($("#exampleInputPassword3")).val()			
		}
		api = "/api-token/login/auth/";
		$http.post(api,{'identification':email,'password':password,'type':type}).then(function(data){
			
			sessionStorage.setItem('Token',data.data.token);
			$http.defaults.headers.common['Authorization'] = 'Token ' + data.data.token;
			window.location.pathname=data.data.redirect_url;
		}, function(rejection) {
			
			if(type=="staff")
				angular.element($("#stafferrid")).removeClass('hide');
			else if(type=='student')
				angular.element($("#studenterrid")).removeClass('hide');
			else
				angular.element($("#teachererrid")).removeClass('hide');
		});
	};
			
	//User details		
   $scope.get_user_details = function(){
   	api = "/api/userdetials"
   	$http.get(api).then(function(result){
   		$scope.profile_details=result.data;
   	});
   };
   
   //Teachers details
   $scope.get_teachres_data = function(searchterm){
   	if(searchterm==undefined)
   		api = "/api/teachersdetails/?searchtearm=all";
   	else
   		api = "/api/teachersdetails/?searchtearm="+searchterm;
   		
   	$http.get(api).then(function(data){
   		$scope.teachersdetails = data.data;
   	});
   };
   
   //students details
   $scope.get_students_data = function(searchterm){
   	
   		if(searchterm==undefined)
   			api = "/api/studentsdetails/?searchtearm=all";
	   	else
	   		api = "/api/studentsdetails/?searchtearm="+searchterm;
	   		
	   	$http.get(api).then(function(data){
	   		$scope.studentsdetails = data.data;
	   	});
   	
   };
   
   //logout 
   $scope.logout = function(){
   	api = "/api/logout"
   	$http.get(api).then(function(result){
   		window.location.pathname="home";
   	});
   };

   //get edit form
   $scope.get_edit_form_data = function(id){
   		id = window.location.search.split('?id=')[1]
   		api = "/api/userdetials/?id="+id
   		$http.get(api).then(function(data){
   			$scope.customObj = data.data;
   		});
   };
  
   //save changes
   $scope.save_edit_Form = function(customObj){
   		if(customObj.user_addressdict.address1==null || customObj.user_addressdict.address2==null || customObj.user_addressdict.city==null){
   			err = angular.element($("#adderr"));
   			err.removeClass('hide');
   		}
   		api = '/api/userdetials/'
   		if(sessionStorage.getItem('change_profile_pic') != undefined){
   			customObj['user_profile_pic1'] = sessionStorage.getItem('change_profile_pic');
   			sessionStorage.removeItem('change_profile_pic');
   		}
   		$http.post(api,customObj,{'headers':{'Authorization':"Token "+sessionStorage.getItem('Token')}}).then(function(data){
   			window.location.pathname="afterlogin";
   		});
   };	
   
   $scope.cancel_form = function(){
   		sessionStorage.removeItem('change_profile_pic');
   		window.location.pathname="afterlogin";
   };

   $scope.search = function(type){
   		searchterm1 = angular.element($("#search_id1")).val();
   		searchterm2 = angular.element($("#search_id2")).val();
   		if(type=='student'){
   			$scope.get_students_data(searchterm2);
   		}else if(type=='teacher'){
			$scope.get_teachres_data(searchterm1);   			
   		}else{
   			$scope.get_teachres_data();
   			$scope.get_students_data();
   		}
   }

   $scope.uploadFile = function(){
       var file = $scope.myFile;
       
       console.log('file is ' );
       console.dir(file);
       
       var uploadUrl = "/api/savemedia/";
       fileUpload.uploadFileToUrl(file, uploadUrl);
    };
					
}]);

