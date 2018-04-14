app.controller("ctrl_model",function($scope,$http){
	url='http://127.0.0.1:8000/home/apid/';
	type="/?format=json";
	//console.log("hello");
	
	$scope.fetch_details=function(id){
		//console.log(url+id+type);
		$('#myModal').modal('show');
		$http.get(url+id+type).success(function(data){
			$scope.s=data;
			//console.log(data);
		})
	}
	
});