const username = localStorage.getItem("username");

if (!username) {
    window.location.href = "login.html";
} else {
    loadProfileData();
}

async function loadProfileData() {
    document.getElementById("displayName").textContent = localStorage.getItem("name") || username;
    document.getElementById("displayEmail").textContent = localStorage.getItem("email") || "Not provided";
    document.getElementById("displayPhone").textContent = localStorage.getItem("phone") || "Not provided";
    document.getElementById("displayOccupation").textContent = localStorage.getItem("occupation") || "Not provided";
    document.getElementById("displayIncome").textContent = localStorage.getItem("income") || "0";

    let apiUrls = [];
    if (window.location.origin && !window.location.origin.startsWith("file") && window.location.origin !== "null") {
        apiUrls.push(`${window.location.origin}/api`);
    }
    apiUrls.push("http://127.0.0.1:8000/api");
    apiUrls.push("http://127.0.0.1:8001/api");
    apiUrls.push("http://localhost:8000/api");
    apiUrls.push("http://localhost:8001/api");

    for (let baseUrl of apiUrls) {
        try {
            const response = await fetch(`${baseUrl}/user/${username}/`);
            if (response.ok) {
                const data = await response.json();
                if (data.user) {
                    if (data.user.email) {
                        document.getElementById("displayEmail").textContent = data.user.email;
                        localStorage.setItem("email", data.user.email);
                    }
                    if (data.user.username && !localStorage.getItem("name")) {
                        document.getElementById("displayName").textContent = data.user.username;
                    }
                }
                break;
            }
        } catch (error) {
            console.warn(`Failed loading user info from ${baseUrl}:`, error);
        }
    }
}

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}