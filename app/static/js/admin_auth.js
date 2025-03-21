document.getElementById('auth-from').addEventListener('submit', async (event) => {
    event.preventDefault();

    let credent = document.getElementById('admin-credentials');
    let password = document.getElementById('admin-password');
    let hint = document.getElementById('invalid-input');
    let isValid;
    let credType;

    if (credent.value.trim() && password.value.trim()) {

        if (credent.value.includes("@")) {
            isValid = validateEmail(credent);
            credType = "email"
        } else {
            isValid = validatePhone(credent);
            credType = "phone"
        }

        if (isValid) {
            let userExists = await findUser(credType, credent.value);
            if (userExists) {
                let isLogged;
                if (credType === "email") {
                    isLogged = await login({email: credent.value, password: password.value});
                } else {
                    isLogged = await login({phone: credent.value, password: password.value});
                }

                if (!isLogged) {
                    hint.style.display = 'block';
                    hint.textContent = "Неправильний пароль!"
                }
                else {
                    window.location.href = '/admin_dashboard';
                }
            }
            else {
                hint.style.display = 'block';
                hint.textContent = "Користувача не знайдено!";
            }
        }
        else {
            let hint = document.getElementById('invalid-input');
            hint.value = 'Неправильна пошта або номер телефону.';
        }
    }
    else {
        let hint = document.getElementById('invalid-input');
        hint.style.display = "block";
        hint.textContent = 'Заповніть всі поля.';
    }
})

function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    let value = email.value;
    if (emailPattern.test(value)) {
        document.getElementById('invalid-input').style.display = 'none';
        return true;
    }
    else {
        let hint = document.getElementById('invalid-input');
        hint.textContent = "Неправильно введена пошта";
        hint.style.display = 'block';
        email.textContent = "";
        return false;
    }
}
function validatePhone(phone) {
    const phonePattern = /^\+?[1-9]\d{1,2}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$/;
    let value = phone.value;
    if (phonePattern.test(value)) {
        document.getElementById('invalid-input').style.display = 'none';
        return true;
    }
    else {
        let hint = document.getElementById('invalid-input');
        hint.textContent = "Неправильно введений номер телефону";
        hint.style.display = 'block';
        phone.textContent = "";
        return false;
    }
}

function findUser(type, value) {
    return fetch('/find_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: type,
            value: value
        })
    })
    .then(res => res.json())
    .then(data => {
        return !!data.success;
    })
    .catch(err => {
        console.log(err);
        return false;
    });
}

function login({email=null, phone=null, password}) {
    return fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            phone: phone,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        return !!data.success;
    })
    .catch(err => {
        console.log(err);
        return false;
    })
}
