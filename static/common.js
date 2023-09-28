let booking=document.querySelector("#booking")
        booking.addEventListener("click",function(){
            if (!token) {
                handleSigninUpButtonClick()
            } else {
                window.location.href="/booking"
            }
        })