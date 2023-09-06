document.addEventListener("DOMContentLoaded",function(){
    let attractionContainer=document.querySelector(".attractions")
    let searchInput=document.getElementById("searchInput")
    let searchButton=document.getElementById("searchButton")

    let nextPage=0
    let isLoading=false
    let currentKeyword=""

    searchButton.addEventListener("click",function(){
    const keyword=searchInput.value.trim()
    if(keyword){
      let containerHeight=attractionContainer.clientHeight
      attractionContainer.innerHTML=""
      attractionContainer.style.height=containerHeight+"px"

      attractionContainer.innerHTML=""
      nextPage=0
      isLoading=false
      currentKeyword=keyword
      loadNextPage(currentKeyword)
    }
  });

    window.addEventListener("scroll",function(){
    let containerRect=attractionContainer.getBoundingClientRect()
    let shouldLoad=containerRect.bottom-window.innerHeight<=200

    if(shouldLoad && !isLoading && nextPage!==null && currentKeyword){
      loadNextPage(currentKeyword)
    }
  });
  function loadNextPage(keyword){
    if(!isLoading && nextPage!==null){
      isLoading=true
      const apiUrl = `/api/attractions?page=${nextPage}&keyword=${keyword}`
      fetch(apiUrl)
        .then((response)=>response.json())
        .then((data)=>{
          if (data && data.data) {
          attractionData = data.data
          if (attractionData.length === 0) {
            attractionContainer.innerHTML="沒有符合的景點"
            
          } else{
          attractionData.forEach((item)=>{
            let attractionElement = document.createElement("div")
            attractionElement.classList.add("attraction")

            let pictureElement = document.createElement("div")
            pictureElement.classList.add("attraction_pic")

            if (item.images && item.images.length>0){
              let firstImage=document.createElement("img")
              firstImage.src=item.images[0]
              pictureElement.appendChild(firstImage)
            }

            let nameElement=document.createElement("div")
            nameElement.classList.add("attraction_name")
            let nameParagraph=document.createElement("p")
            nameParagraph.textContent=item.name;
            nameElement.appendChild(nameParagraph)

            let mrtElement=document.createElement("div")
            mrtElement.classList.add("attraction_bottom")
            let mrtParagraph = document.createElement("p")
            mrtParagraph.textContent=item.mrt
            mrtElement.appendChild(mrtParagraph)

            let catParagraph=document.createElement("p")
            catParagraph.textContent=item.category
            mrtElement.appendChild(catParagraph)

            attractionElement.appendChild(pictureElement)
            attractionElement.appendChild(nameElement)
            attractionElement.appendChild(mrtElement)

            attractionContainer.appendChild(attractionElement)
          })
          
          if (attractionData.length<13 || nextPage!==null && attractionData.length>0){
            nextPage=data.nextPage
          } else {
            nextPage=null
           
          }
        }}
        isLoading=false
        attractionContainer.style.height="auto"
        
      })
     
  }
}

});