async function login() {
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value;
    let message = document.getElementById("message");

    if (email == "" || password == "") {
        message.style.color = "red";
        message.innerHTML = "Please fill all the fields.";
        return;
    }

    let apiUrls = [];
    if (window.location.origin && !window.location.origin.startsWith("file") && window.location.origin !== "null") {
        apiUrls.push(`${window.location.origin}/api`);
    }
    apiUrls.push("http://127.0.0.1:8000/api");
    apiUrls.push("http://127.0.0.1:8001/api");
    apiUrls.push("http://localhost:8000/api");
    apiUrls.push("http://localhost:8001/api");

    let response = null;
    let data = null;

    for (let baseUrl of apiUrls) {
        try {
            response = await fetch(`${baseUrl}/login/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: email,
                    email: email,
                    password: password
                })
            });
            data = await response.json();
            break;
        } catch (err) {
            console.warn(`Could not connect to ${baseUrl}:`, err);
        }
    }

    if (!response || !data) {
        message.style.color = "red";
        message.innerHTML = "Something went wrong connecting to backend.";
        return;
    }

    if (response.ok) {
        message.style.color = "green";
        message.innerHTML = "Login successful!";

        const username = data.username || email;
        localStorage.setItem("username", username);
        localStorage.setItem("name", username);

        setTimeout(() => {
            window.location.href = "index.html";
        }, 400);
    } else {
        message.style.color = "red";
        message.innerHTML = data.error || "Invalid login credentials.";
    }
}
