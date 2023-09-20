
let overlay=document.querySelector(".overlay")
let signinUpButton=document.getElementById("signin_up")
let signinContainer=document.querySelector(".signinContainer")
let signupContainer=document.querySelector(".signupContainer")
let close_in=document.querySelector(".close_in")
let close_up=document.querySelector(".close_up")


let isLoggedIn=false


let signupForm=document.querySelector("#signupForm")
let signupMessage=document.createElement("div")
signupMessage.classList.add("signup-message")

signupForm.addEventListener("submit",function(e){
    e.preventDefault()
    let signUpName=document.querySelector("#signUpName").value
    let signUpEmail=document.querySelector("#signUpEmail").value
    let signUpPassword=document.querySelector("#signUpPassword").value

    if (!signUpName || !signUpEmail || !signUpPassword) {
        signupMessage.textContent="欄位請完整填寫";
        signupMessage.style.color="red";
        toSignin.insertAdjacentElement("beforebegin",signupMessage);
        return
    }

    fetch("/api/user",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
        },
        body:JSON.stringify({
            name:signUpName,
            email:signUpEmail,
            password:signUpPassword
        }),
    })
    .then(response=>{
        return response.json()
    })
    .then(data=>{
        if(data.ok){
            signupMessage.textContent="註冊成功"
            signupMessage.style.color="green"
        }else{
            signupMessage.textContent="註冊失敗，重複的Email或其他原因"
            signupMessage.style.color="red"
        }
        document.querySelector("#signUpName").value =""
        document.querySelector("#signUpEmail").value = ""
        document.querySelector("#signUpPassword").value = ""
        toSignin.insertAdjacentElement("beforebegin",signupMessage)
    })
})




let signinForm = document.querySelector("#signinForm")
let toSignup =document.querySelector(".toSignup")
let signinMessage = document.createElement("div")
signinMessage.classList.add("signin-message")

signinForm.addEventListener("submit",function(e){
    e.preventDefault()
    signinMessage.textContent=""
    signinMessage.style.color=""
    
    let signInEmail=document.querySelector("#signInEmail").value
    let signInPassword=document.querySelector("#signInPassword").value

    if(!signInEmail || !signInPassword){
        signinMessage.textContent="欄位請完整填寫"
        signinMessage.style.color="red"
        toSignup.insertAdjacentElement("beforebegin",signinMessage)
        return
    }
   
    
    fetch("/api/user/auth",{
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            email:signInEmail,
            password:signInPassword})
    })
    .then(response=>{
        if (response.status===200){
            return response.json()
        } else {
            signinMessage.textContent="登入失敗"
            signinMessage.style.color="red"
            setTimeout(()=>{
                signinMessage.textContent=""
            }, 5000)
        }
    })
    .then(data=>{
        if (data&&data.token){
            localStorage.setItem("token",data.token)
            isLoggedIn=true
            let currentURL=window.location.href
            window.location.href=currentURL
        } 
        document.querySelector("#signInPassword").value=""
        document.querySelector("#signInEmail").value=""
        toSignup.insertAdjacentElement("beforebegin",signinMessage)
    }) 
})    

let token=localStorage.getItem("token")
fetch("/api/user/auth",{
    method:"GET",
    headers:{
        "Authorization":`Bearer ${token}`
    }
})
.then(response=>{
    if (response.status === 200){
        return response.json()
    } else{
        throw new Error("")
    }
})
.catch(error => {
    console.error("API請求錯誤", error)
   
});

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