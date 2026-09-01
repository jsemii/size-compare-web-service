const token = localStorage.getItem("token");
console.log(token);

const btn = document.getElementById("register-btn");

function toCm(value) {
    if (!value) return value;
    const unit = document.getElementById("unit-select").value;
    if (unit == "inch") return value / 2.54;
    return value;
}

btn.addEventListener("click", async function () {
    const name = document.getElementById("name").value;
    const category = document.getElementById("category").value;
    const total_length_cm = document.getElementById("total_length_cm").value;
    const shoulder_cm = document.getElementById("shoulder_cm").value;
    const chest_cm = document.getElementById("chest_cm").value;
    const sleeve_cm = document.getElementById("sleeve_cm").value;
    const waist_cm = document.getElementById("waist_cm").value;
    const hip_cm = document.getElementById("hip_cm").value;

    const body = { name: name, category: category };

    if(total_length_cm) body.total_length_cm = toCm(total_length_cm);
    if(shoulder_cm) body.shoulder_cm = toCm(houlder_cm);
    if(chest_cm) body.chest_cm = toCm(chest_cm);
    if(sleeve_cm) body.sleeve_cm = toCm(sleeve_cm);
    if(waist_cm) body.waist_cm = toCm(waist_cm);
    if(hip_cm) body.hip_cm = toCm(hip_cm);

    const response = await fetch("/api/garments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(body)
    });

    const data = await response.json();
    console.log(data);

    // 등록 성공했고, 사진을 골랐으면 → 사진 업로드
    const photoInput = document.getElementById("photo");
    if (response.ok && photoInput.files.length > 0) {
        const garmentId = data.id;                    // 등록 응답에서 id 받기
        const formData = new FormData();
        formData.append("file", photoInput.files[0]); // 고른 사진 파일

        const photoResponse = await fetch(`/api/garments/${garmentId}/photo`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
                // ⚠️ Content-Type 넣지 마! FormData가 알아서 설정함
            },
            body: formData
        });
        console.log("사진 업로드:", photoResponse.status);
    }

    document.getElementById("message").textContent = `상태코드: ${response.status}`;
});

    document.getElementById("main-btn").addEventListener("click", function () {
        window.location.href = "main.html";
    });