const garmentsBtn = document.getElementById("btn-garments");
const wishlistBtn = document.getElementById("btn-wishlist");
const token = localStorage.getItem("token");

garmentsBtn.addEventListener("click", async function () {
    window.location.href = "garments.html";
});

wishlistBtn.addEventListener("click", () => {
    window.location.href = "wishlist.html";
});

async function loadGarments() {
    const response = await fetch("http://127.0.0.1:8000/garments", {
        headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await response.json();
    console.log(data);

    const select = document.getElementById("garment-select");

    for (const garment of data) {
        const option = document.createElement("option");
        option.value = garment.id;
        option.textContent = garment.name;
        select.appendChild(option);
    }
}
loadGarments();

async function loadWishlists() {
    const response = await fetch("http://127.0.0.1:8000/wishlists", {
        headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await response.json();
    console.log(data);

    const select = document.getElementById("wishlist-select");

    for (const wishlist of data) {
        const option = document.createElement("option");
        option.value = wishlist.id;
        option.textContent = wishlist.name;
        select.appendChild(option);
    }
}
loadWishlists();

const compareBtn = document.getElementById("compare-btn");

compareBtn.addEventListener("click", async function () {
    const garmentId = document.getElementById("garment-select").value;
    const wishlistId = document.getElementById("wishlist-select").value;

    const response = await fetch(`http://127.0.0.1:8000/compare?garment_id=${garmentId}&wishlist_id=${wishlistId}`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const data = await response.json();
    console.log(data);

    const result = document.getElementById("result");

    let html = "<table border='1'>";
    html += "<tr><td>항목</td><td>내 옷</td><td>위시</td><td>차이</td></tr>";

    const fieldNames = {
        total_length: "총길이",
        shoulder: "어깨너비",
        chest: "가슴단면",
        sleeve: "소매길이",
        waist: "허리단면",
        hip: "엉덩이단면"
    };

    for (const item of data.items) {
        if (!item.comparable) continue;

        html += "<tr>";
        html += `<td>${fieldNames[item.field]}</td>`;
        html += `<td>${item.my_cloth}</td>`;
        html += `<td>${item.wish_cloth}</td>`;
        html += `<td>${item.diff}</td>`;
        html += "</tr>";
    }

    html += "</table>";
    result.innerHTML = html;
});