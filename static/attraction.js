document.addEventListener("DOMContentLoaded",function(){
  
  let orderButton = document.querySelector(".order_botton")
    if (orderButton){
        orderButton.addEventListener("click",function(){
            if(!token){
                handleSigninUpButtonClick()
            }else{
            let orderDate=document.querySelector("#ordet_date").value
            let currentUrl=window.location.pathname
            let id=currentUrl.split('/').pop()
            let tourFeeText=document.querySelector("#tour_fee").textContent
            let tourFee=parseInt(tourFeeText.match(/\d+/)[0])
            function getSelectedTime(){
                let selectedTime;
                if (tourFee == 2000){
                    selectedTime="上半天"
                } else {
                    selectedTime="下半天"
                }
                return selectedTime
            }
            fetch("/api/booking",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization":`Bearer ${token}`,
                },
                body:JSON.stringify({
                    id:id,
                    date:orderDate,
                    time:getSelectedTime(),
                    price:tourFee,
                })
            }).then((response)=>{
                return response.json()
            }).then((data) => {
                window.location.href = "/booking";
            });}});}
    if (window.location.pathname.includes('/attraction/')){
    let attractionId=window.location.pathname.split('/').pop()
    let apiUrl=`/api/attraction/${attractionId}`
  
    fetch(apiUrl)
    .then((response)=>response.json()) 
    .then((data)=>{console.log(data)
      if (data && data.name){
        let titleElement=document.createElement("p")
        titleElement.textContent=data.name
        let titleContainer=document.querySelector(".title")
        titleContainer.appendChild(titleElement)

        let subtitleContainer=document.querySelector(".subtitle")
        let catElement=document.createElement("p")
        catElement.textContent=data.category
        subtitleContainer.appendChild(catElement)
       
        let atSpan=document.createElement("span")
        atSpan.textContent= " at "
        atSpan.classList.add("at-text")
        subtitleContainer.appendChild(atSpan)

       
        let mrtElement=document.createElement("p")
        mrtElement.textContent=data.mrt
        subtitleContainer.appendChild(mrtElement)
        
        let inforContainer=document.querySelector(".info_content")
        let inforElement=document.createElement("p")
        inforElement.textContent=data.description
        inforContainer.appendChild(inforElement)

        let adressElement=document.querySelector(".adress")
        let newParagraph=document.createElement("p")
        newParagraph.classList.add("adress")
        newParagraph.textContent=data.address
        adressElement.replaceWith(newParagraph)

        let trafficElement=document.querySelector(".traffic")
        let trafficParagraph=document.createElement("p")
        trafficParagraph.classList.add("traffic")
        trafficParagraph.textContent=data.transport
        trafficElement.replaceWith(trafficParagraph)


        if (data.images && data.images.length>0){
            let imageCount=data.images.length
            let currentIndex=0
            let currentImage=document.createElement("img")
            currentImage.classList.add("bg")
            currentImage.src=data.images[0]
            document.querySelector(".section_image").appendChild(currentImage)
        
            let dotContainer=document.querySelector(".current")
            for (let i=0;i<imageCount;i++){
                let dot=document.createElement("img")
                dot.src="/static/images/circle_notcurrent.svg"
                dot.classList.add("dot")
                dot.addEventListener("click",() =>showImage(i))
                dotContainer.appendChild(dot)
            }

            function showImage(imageIndex) {
                let dots=document.querySelectorAll(".dot")
                dots.forEach((dot,index)=>{
                    dot.src=index===imageIndex
                        ? "/static/images/circle_current.svg"
                        : "/static/images/circle_notcurrent.svg"
                })
                    currentImage.src=data.images[imageIndex]
                    currentImage.style.transition="opacity 0.5s ease-in-out"
                    currentImage.style.opacity=1
                    currentIndex=imageIndex
            }
            showImage(currentIndex)
        
            const prevButton=document.querySelector(".left_arror")
            const nextButton=document.querySelector(".right_arror")
        
            prevButton.addEventListener("click",()=>{
                currentIndex=(currentIndex-1+ imageCount)%imageCount
                currentImage.style.transition="opacity 0.5s ease-in-out"
                currentImage.style.opacity=0
                setTimeout(()=>{
                  showImage(currentIndex)
                },500)
              })
              
              nextButton.addEventListener("click",()=>{
                currentIndex=(currentIndex+1)%imageCount
                currentImage.style.transition="opacity 0.5s ease-in-out"
                currentImage.style.opacity=0
                setTimeout(()=>{
                  showImage(currentIndex)
                },500)
              })
              
        }
        
        let chooseTime1=document.querySelector(".choose_time:nth-child(2)")
        let chooseTime2=document.querySelector(".choose_time:nth-child(3)")
    
        let tourFeeElement=document.getElementById("tour_fee")
        tourFeeElement.textContent=`新台幣 2000 元`
      
        let btnImage1=chooseTime1.querySelector("img")
        let btnImage2=chooseTime2.querySelector("img")
    
        chooseTime1.addEventListener("click",function(){
            btnImage1.src="/static/images/radio btn.svg"
            btnImage2.src="/static/images/radio btn_off.svg"
            tourFee = 2000
            tourFeeElement.textContent=`新台幣 ${tourFee} 元`
        })
        chooseTime2.addEventListener("click",function(){
            btnImage1.src="/static/images/radio btn_off.svg"
            btnImage2.src="/static/images/radio btn.svg"
            tourFee=2500
            tourFeeElement.textContent=`新台幣 ${tourFee} 元`
        })
    } 
})
    }
    }
)

    


    
