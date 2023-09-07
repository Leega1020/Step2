document.addEventListener("DOMContentLoaded",function(){
    let mrtList=document.getElementById("mrt_list")
    let scrollLeftButton=document.getElementById("scroll-left")
    let scrollRightButton=document.getElementById("scroll-right")
    let searchInput=document.getElementById("searchInput")
    let searchButton=document.getElementById("searchButton")
    let list_item=document.querySelector(".list_item")

    let searching=false
    let itemWidth=calculateItemWidth()
    let scrollPosition=0

    function calculateItemWidth(){
        let windowWidth=window.innerWidth;
        if (windowWidth<600){
            return 200
        }else if (windowWidth>=600 && windowWidth<=1200){
            return 600
        }else {
            return 1000
        }
    }
    

    fetch("/api/mrts")
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
                    })
                    mrtList.appendChild(button)
                });
                const maxScrollPosition=Math.max(0,mrtList.scrollWidth-mrtList.offsetWidth)
                function updateList(){
                    if (itemWidth>=mrtList.offsetWidth){
                        scrollPosition=maxScrollPosition
                        startSearch()
                        
                    }
                    if (scrollPosition===maxScrollPosition){
                        scrollRightButton.disabled=true
                    } else {
                        scrollRightButton.disabled=false
                    }
                    //mrtList.style.transform=`translateX(-${scrollPosition}px)`
                }
                function startSearch(){
                    searching=true    
                }

                updateList()

                scrollLeftButton.addEventListener("click",()=>{
                    if (scrollPosition>0){
                        scrollPosition-=itemWidth
                        list_item.scrollTo({
                            left:scrollPosition,
                            behavior:"smooth",
                        });
                        if (scrollPosition<0){
                            scrollPosition=0
                        }
                    }
                    updateList()

                    if (scrollPosition===0){
                        scrollLeftButton.disabled=true
                        list_item.scrollTo({
                            left:scrollPosition,
                            behavior:"smooth",
                        });
                    }
                    scrollRightButton.disabled=false
                });

                scrollRightButton.addEventListener("click",()=>{
                    if(scrollPosition<maxScrollPosition){
                        scrollPosition+=itemWidth
                        list_item.scrollTo({
                            left:scrollPosition,
                            behavior:"smooth",
                        });
                        if (scrollPosition>maxScrollPosition){
                            scrollPosition=maxScrollPosition
                        }
                    }
                    updateList()
                    if (scrollPosition===maxScrollPosition) {
                        scrollRightButton.disabled=true
                        list_item.scrollTo({
                            left:scrollPosition,
                            behavior:"smooth",
                        });
                    }
                    scrollLeftButton.disabled=false
                });
            }
        });

    
});