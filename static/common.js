

let signinUpButton=document.getElementById("signin_up")
let signinContainer=document.querySelector(".signinContainer")
let signupContainer=document.querySelector(".signupContainer")
let close_in=document.querySelector(".close_in")
let close_up=document.querySelector(".close_up")

let booking=document.querySelector("#booking")
let isLoggedIn = false;


function handleSigninUpButtonClick() {
    if (isLoggedIn){
        signinContainer.style.display="flex"
        overlay.style.display="block"
        setTimeout(function(){
            signinContainer.style.transition="transform 0.5s ease-in"
            signinContainer.style.transform="translate(-50%, 80px)"
        },0)
        
    }else{
        let token=localStorage.getItem("token")
        
        if(token){
            isLoggedIn=false
            localStorage.removeItem("token")
            localStorage.removeItem("User-Name")
            localStorage.removeItem("id")
            localStorage.removeItem("name")
            localStorage.removeItem("address")
            localStorage.removeItem("image")
            localStorage.removeItem("date")
            localStorage.removeItem("time")
            localStorage.removeItem("price")
            localStorage.removeItem("orderNumber")
            window.location.reload()
        }else{
            isLoggedIn=true
        }
    }
    updateLoginButton()
}

signinUpButton.addEventListener("click",handleSigninUpButtonClick)

function updateLoginButton() {
    let token=localStorage.getItem("token")
    if (token){
        signinUpButton.textContent="登出系統"
    } else {
        signinUpButton.textContent="登入/註冊"
    }
}
updateLoginButton()


let signupLink=document.getElementById("signupLink")
signupLink.addEventListener("click",()=>{
    signupContainer.style.display="block"
    signinContainer.style.display="none"
});
let toSignin=document.querySelector(".toSignin")
toSignin.addEventListener("click",function(){
    signupContainer.style.display="none"
    signinContainer.style.display="block"
})


close_in.addEventListener("click",()=>{
    signinContainer.style.display="none"
    overlay.style.display = "none"
});

close_up.addEventListener("click",()=>{
    signupContainer.style.display="none"
    overlay.style.display="none"
});




        booking.addEventListener("click",function(){
            let token=localStorage.getItem("token")
            if (!token) {
                handleSigninUpButtonClick()
            } else {
                window.location.href="/booking"
            }
        })