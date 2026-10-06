async function register() {
    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;
    let message = document.getElementById("message");

    if (name == "" || email == "" || password == "") {
        message.style.color = "red";
        message.innerHTML = "Please fill all the fields.";
        return;
    }

    if (password !== confirmPassword) {
        message.style.color = "red";
        message.innerHTML = "Passwords do not match.";
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
            response = await fetch(`${baseUrl}/register/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: name,
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
        message.innerHTML = "Registration successful!";

        const registeredUser = data.username || name;
        localStorage.setItem("username", registeredUser);
        localStorage.setItem("name", name);
        if (email) localStorage.setItem("email", email);

        setTimeout(() => {
            window.location.href = "index.html";
        }, 400);
    } else {
        message.style.color = "red";
        message.innerHTML = data.error || "Registration failed.";
    }
}
