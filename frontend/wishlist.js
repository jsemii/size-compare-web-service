const token = localStorage.getItem("token");
console.log(token);

const btn = document.getElementById("register-btn");

btn.addEventListener("click", async function () {
    const name = document.getElementById("name").value;
    const category = document.getElementById("category").value;
    const shop_name = document.getElementById("shop_name").value;
    const total_length_cm = document.getElementById("total_length_cm").value;
    const shoulder_cm = document.getElementById("shoulder_cm").value;
    const chest_cm = document.getElementById("chest_cm").value;
    const sleeve_cm = document.getElementById("sleeve_cm").value;
    const waist_cm = document.getElementById("waist_cm").value;
    const hip_cm = document.getElementById("hip_cm").value;

    const body = { name: name, category: category, shop_name: shop_name };

    if(total_length_cm) body.total_length_cm = total_length_cm;
    if(shoulder_cm) body.shoulder_cm = shoulder_cm;
    if(chest_cm) body.chest_cm = chest_cm;
    if(sleeve_cm) body.sleeve_cm = sleeve_cm;
    if(waist_cm) body.waist_cm = waist_cm;
    if(hip_cm) body.hip_cm = hip_cm;

    const response = await fetch("http://127.0.0.1:8000/wishlists", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(body)
    });

    const data = await response.json();
    console.log(data);

    document.getElementById("message").textContent = `상태코드: ${response.status}`;
});