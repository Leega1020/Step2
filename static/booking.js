document.addEventListener("DOMContentLoaded",function(){
        let token = localStorage.getItem("token")
        let User_Name=localStorage.getItem("User-Name")
        if (!token) {
            window.location.href = "/"
        }else{
            getData()

        function getData(){

            fetch("/api/booking",{
                method:"GET",
                headers:{
                    "Authorization":`Bearer ${token}`,
                },
            })
            .then((response)=>{
                if(response.status===200){
                    return response.json()
                } else{
                    throw new Error("Failed to fetch data")
                }
            })
            .then((data)=>{
                if (token){
                    if (data.data!==null){
                        let scheduleData=data.data
                        let dataElement=document.querySelector("#date")
                        dataElement.textContent=scheduleData.date
                        let timeElement=document.querySelector("#time")
                        timeElement.textContent=scheduleData.time
                        let priceElement=document.querySelector("#price")
                        priceElement.textContent=scheduleData.price;
                        let locatElement=document.querySelector("#locat")
                        locatElement.textContent=scheduleData.attraction.address
                        let nameElement=document.querySelector("#title")
                        nameElement.textContent=scheduleData.attraction.name
                        let totalElement=document.querySelector("#total")
                        totalElement.textContent=scheduleData.price
                        let imgElement=document.createElement("img")
                        let imgElementContainer=document.querySelector(".booking_img")
                        imgElement.src=scheduleData.attraction.image
                        imgElementContainer.appendChild(imgElement)
                        let user_nameElement=document.querySelector("#user_name")
                        user_nameElement.textContent=User_Name
                    } else {
                        let main=document.querySelector("main")
                        main.innerHTML=""
                        let user_nameElement=document.querySelector("#user_name")
                        user_nameElement.textContent=User_Name
                        let emptyContent=document.querySelector("#emptyBooking")
                        emptyContent.textContent="目前沒有任何待預訂的行程"
                    }
                }
            })
            .catch((error)=>{
                console.error(error)
            })  
        }}

    let trash=document.querySelector(".trash")
    trash.addEventListener("click",function(){
        let token=localStorage.getItem("token")
        if(!token){
            handleSigninUpButtonClick()
        }else{
            fetch("api/booking",{
                method:"DELETE",
                headers:{
                    "Authorization":`Bearer ${token}`
                }
            })
            .then((response)=>{
                if(response.status===200) {
                    console.log(response)
                    window.location.reload()
                }else{
                    throw new Error("Failed to delete booking")
                }
            })
            .catch((error)=>{
                console.error(error)
            })
        }
    });
});
    
    