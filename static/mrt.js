document.addEventListener("DOMContentLoaded",function(){
    let mrtList = document.getElementById("mrt_list")
    let scrollLeftButton = document.getElementById("scroll-left")
    let scrollRightButton = document.getElementById("scroll-right")
    let searchInput = document.getElementById("searchInput")
    let searchButton = document.getElementById("searchButton")
    let contentContainer = document.querySelector(".attractions")

    let searching=false
    let itemWidth=1000
    let scrollPosition=0

    fetch("http://127.0.0.1:3000/api/mrts")
        .then((response)=>response.json())
        .then((data)=>{
            if (data && data.data && Array.isArray(data.data)){
                let attractionData=data.data
                attractionData.forEach(item=>{
                    let button = document.createElement("button")
                    button.textContent=item
                    button.addEventListener("click",()=>{
                        searchInput.value = item
                        searchButton.click()
                        generateContent(item)
                    })
                    mrtList.appendChild(button)
                });
                const maxScrollPosition=Math.max(0,mrtList.scrollWidth-mrtList.offsetWidth)
                function updateList(){
                    if (itemWidth>=mrtList.offsetWidth){
                        scrollPosition=maxScrollPosition
                        startSearch()
                        performSearch()
                    }
                    if (scrollPosition===maxScrollPosition){
                        scrollRightButton.disabled=true
                    } else {
                        scrollRightButton.disabled=false
                    }
                    mrtList.style.transform=`translateX(-${scrollPosition}px)`
                }
                function startSearch(){
                    searching=true
                    window.removeEventListener("scroll",loadNextPage)
                    contentContainer.innerHTML=""
                }

                updateList()

                scrollLeftButton.addEventListener("click",()=>{
                    if(scrollPosition>0){
                        scrollPosition-=itemWidth
                    }else{
                        scrollPosition=0
                    }
                    updateList()
                });

                scrollRightButton.addEventListener("click",()=>{
                    if(scrollPosition<maxScrollPosition){
                        scrollPosition+=itemWidth
                        if (scrollPosition>maxScrollPosition){
                            scrollPosition=maxScrollPosition
                        }
                    }
                    updateList()
                });
            }
        })
      
    function generateContent(selectedItem){
        contentContainer.innerHTML=""
        isLoading=true
    }  
});




