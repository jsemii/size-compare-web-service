const btn = document.getElementById("login-btn");

btn.addEventListener("click", async function () {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, password: password })
    });

    if (response.ok) {
    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    window.location.href = "garments.html";
    
} else {
    document.getElementById("message").textContent = "이메일 또는 비밀번호가 틀렸습니다";
    
}
});