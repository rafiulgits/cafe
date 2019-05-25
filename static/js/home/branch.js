function addToCart(branch_food_id, branch_id, detail){
	fetch('/cart/add/?branch_food_id='+branch_food_id+'&branch_id='+branch_id)
	.then(response => response.text())
	.then(data => {
		if(data == 'Ok'){
			var ele = document.getElementById(detail);
			var x = ele.innerHTML;
			var arr = x.split(': ');
			var quantity = parseInt(arr[1]);
			ele.innerHTML = 'Quantity: '+new String(quantity+1);
		}
		else{

		}
	})
	.catch((error) => {
  		console.log(error);
	});
}