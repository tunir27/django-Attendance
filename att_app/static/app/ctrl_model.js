app.controller("ctrl_model",function($scope,$http){
	url='https://attendanceproject.herokuapp.com/dashboard/apid/';
	//type="/?format=json";
	//console.log("hello");
	
	$scope.fetch_details=function(id){
		console.log(id);
		$('#myModal').modal('show');
		$http.get(url+id).success(function(data){
			$scope.s=data;
			console.log(data);
		})
	}
	
});