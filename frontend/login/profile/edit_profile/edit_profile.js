window.onload = function() {
    document.getElementById("name").value = localStorage.getItem("name") || localStorage.getItem("username") || "";
    document.getElementById("email").value = localStorage.getItem("email") || "";
    document.getElementById("phone").value = localStorage.getItem("phone") || "";
    document.getElementById("occupation").value = localStorage.getItem("occupation") || "";
    document.getElementById("income").value = localStorage.getItem("income") || "";
};

function saveProfile() {
    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let occupation = document.getElementById("occupation").value.trim();
    let income = document.getElementById("income").value.trim();

    if (name === "" || email === "") {
        alert("Please enter Name and Email.");
        return;
    }

    localStorage.setItem("name", name);
    localStorage.setItem("email", email);
    localStorage.setItem("phone", phone);
    localStorage.setItem("occupation", occupation);
    localStorage.setItem("income", income);

    alert("Profile saved successfully!");
    window.location.href = "../profile/profile.html";
}