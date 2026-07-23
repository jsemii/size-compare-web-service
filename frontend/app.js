const btn = document.getElementById("login-btn");

btn.addEventListener("click", async function () {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, password: password })
    });

    const data = await response.json();
    console.log(data);

    localStorage.setItem("token", data.access_token);

    document.getElementById("message").textContent = `상태코드: ${response.status}`;
});