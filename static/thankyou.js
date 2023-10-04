function getOrderDetails(orderNumber) {
    let token = localStorage.getItem('token')
    if (!token) {
        window.location.href = "/";
        return;
    }
    fetch(`/api/orders/${orderNumber}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "Authorization":`Bearer ${token}`
           
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
       if(data.data==null){
        window.location.href="/"
       }else{
        window.location.href=`/thankyou?number=${orderNumber}`}
       
    })
    .catch(error => {
        console.error('Error:', error);
    });}
    