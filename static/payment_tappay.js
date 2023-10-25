document.addEventListener("DOMContentLoaded",function(){
    window.print=function(){ }
    if(token){
    //let PARTNER_KEY="partner_7YCCWUrfOcTjoZebBvVp1Y1ehH1uZbzPsHd3I5sBitpxN5ZwCNJwtTg3"
    fetch('/api/config')
        .then(response => response.json())
        .then(data => {
            const APP_ID=data.APP_ID
            const APP_KEY=data.APP_KEY
            TPDirect.setupSDK(APP_ID, APP_KEY,"sandbox")
            
        })

const submitButton = document.getElementById('submit-button')
submitButton.addEventListener('click', onSubmit);
let fields = {
    number: {
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: '後三碼'
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'color': 'gray'
        },
        'input.ccv': {
            // 'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            // 'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            // 'font-size': '16px'
        },
        // style focus state
        ':focus': {
           'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6, 
        endIndex: 11
    }
})


TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        // submitButton.removeAttribute('disabled')
    } else {
        // Disable submit Button to get prime.
        // submitButton.setAttribute('disabled', true)
    }
                                            
    // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unknown']
    if (update.cardType === 'visa') {
        // Handle card type visa.
    }

    // number 欄位是錯誤的
    if (update.status.number === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.number === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }
    
    if (update.status.expiry === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.expiry === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }
    
    if (update.status.ccv === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.ccv === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }
})

function onSubmit(event) {
    event.preventDefault()

    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    if (tappayStatus.canGetPrime === false) {
        alert('can not get prime')
        return
    }

    TPDirect.card.getPrime(function(result) {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }
        //console.log(result.card.prime)
        //console.log(result)
        fetch('/api/config')
        .then(response => response.json())
        .then(data => {
            const PARTNER_KEY=data.PARTNER_KEY
            
        
        let token = localStorage.getItem("token")
        let id=localStorage.getItem("id")
        let name=localStorage.getItem("name")
        let address=localStorage.getItem("address")
        let image=localStorage.getItem("image")
        let date=localStorage.getItem("date")
        let time=localStorage.getItem("time")
        let price=localStorage.getItem("price")

        let contactName=document.querySelector("#contactName").value
        let contactMail=document.querySelector("#contactMail").value
        let contactPhone=document.querySelector("#contactPhone").value
        const requestData = {
            "prime": result.card.prime,

            "order": {
              "price": price,
              "trip": {
                "attraction": {
                  "id": id,
                  "name": name,
                  "address": address,
                  "image": image
                },
                "date": date,
                "time": time
              },
              "contact": {
                "name": contactName,
                "email": contactMail,
                "phone":contactPhone
              }
            }
        }

   
        fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization":`Bearer ${token}`,
                "x-api-key":PARTNER_KEY
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            let orderNumber=data.data.number
            localStorage.setItem("orderNumber",orderNumber)
            localStorage.removeItem("date")
            localStorage.removeItem("time")
            localStorage.removeItem("id")
            localStorage.removeItem("address")
            localStorage.removeItem("image")
            localStorage.removeItem("name")
            localStorage.removeItem("price")
            getOrderDetails(orderNumber)

        })
        .catch(error => {
            console.error('Error:', error);
        })})
    })
}}})