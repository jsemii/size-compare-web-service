const btn = document.getElementById("login-btn");

btn.addEventListener("click", async function () {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, password: password })
    });

    if (response.ok) {
    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    window.location.href = "main.html";
    
} else {
    document.getElementById("message").textContent = "이메일 또는 비밀번호가 틀렸습니다";
    
}
});

const passwordInput = document.getElementById("password");

passwordInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        btn.click();
    }
});