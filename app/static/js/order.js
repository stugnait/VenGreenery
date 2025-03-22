document.getElementById('input-form').addEventListener('submit', event => {
    event.preventDefault();

    const emailValue = document.getElementById('user-email').value;
    const phoneValue = document.getElementById('user-phone').value;
    const adultQuantityValue = document.getElementById('adult-quantity').value;
    const childQuantityValue = document.getElementById('child-quantity').value;
    const userSurnameValue = document.getElementById('user-surname').value;
    const userNameValue = document.getElementById('user-name').value;

    let hint = document.getElementById('invalid-input');

    if (!validateEmail(emailValue)) {
        hint.style.display = 'block';
        hint.textContent = "Неправильно введена пошта";
    }
    else if (!validatePhone(phoneValue)) {
        hint.style.display = 'block';
        hint.textContent = "Неправильно введений номер телефону"
    }
    else if (!validateQuantity(adultQuantityValue, childQuantityValue)) {
        hint.style.display = 'block';
        hint.textContent = "Лише один квиток"
    }
    else if (!validateFullName(userNameValue, userSurnameValue)) {
        hint.style.display = 'block';
        hint.textContent = "Заповніть поле імені та прізвища"
    }
    else {
        hint.style.display = 'none';
        console.log("GONNA FETCH")
        fetch("/order", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: userNameValue,
                surname: userSurnameValue,
                email: emailValue,
                phone: phoneValue,
                ticket_type: adultQuantityValue === 1 ? "adult" : "child"
            })
        })
        .then(res => res.json())
        .then(data => {
            window.location.href = data;
        })
        .catch(err => console.log(err));


    }


})

function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}
function validatePhone(phone) {
    const phonePattern = /^\+?[1-9]\d{1,2}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/;
    return phonePattern.test(phone);
}

function validateQuantity(adult, child) {
    return (adult === "1" && child === "0") || (adult === "0" && child === "1");
}

function validateFullName(name, surname) {
    return name.trim().length > 0 && surname.trim().length > 0;
}

