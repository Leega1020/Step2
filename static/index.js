document.addEventListener("DOMContentLoaded",function(){
  let nextPage=0
  let threshold=200
  
  let isLoading=false;
  let attractionContainer=document.querySelector(".attractions")

  if (attractionContainer){
    window.addEventListener("scroll",()=>{
      if (nextPage!==null&&!isLoading){
        let containerRect=attractionContainer.getBoundingClientRect()
        let loadData=containerRect.bottom-window.innerHeight<=threshold

        if(loadData){
          isLoading=true 
          loadNextPage()
        }
      }
    });
  }

  function loadNextPage(){
      fetch(`http://127.0.0.1:3000/api/attractions?page=${nextPage}`)
        .then((response)=>response.json())
        .then((data)=>{
          if (data && data.data) {
            let attractionData=data.data
            attractionData.forEach(item=>{
                let attractionElement=document.createElement("div")
                attractionElement.classList.add("attraction")

                let pictureElement=document.createElement("div")
                pictureElement.classList.add("attraction_pic")

                if (item.images && item.images.length>0){
                  let firstImage=document.createElement("img")
                  firstImage.src=item.images[0]
                  pictureElement.appendChild(firstImage)
                }

                let nameElement=document.createElement("div")
                nameElement.classList.add("attraction_name")
                let nameParagraph=document.createElement("p")
                nameParagraph.textContent=item.name
                nameElement.appendChild(nameParagraph)
                
                let mrtElement=document.createElement("div")
                mrtElement.classList.add("attraction_bottom")
                let mrtParagraph=document.createElement("p")
                mrtParagraph.textContent=item.mrt
                mrtElement.appendChild(mrtParagraph)
                
                let catParagraph=document.createElement("p")
                catParagraph.textContent=item.category
                mrtElement.appendChild(catParagraph)
                
                attractionElement.appendChild(pictureElement)
                attractionElement.appendChild(nameElement)
                attractionElement.appendChild(mrtElement)
                
                attractionContainer.appendChild(attractionElement)
            });
            
            if (attractionData.length<13 || nextPage!==null){
              nextPage = data.nextPage
            }
            else{
              nextPage=null
            }
          }isLoading=false
        });
    }loadNextPage()
  });
  

