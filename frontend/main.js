const garmentsBtn = document.getElementById("btn-garments");
const wishlistBtn = document.getElementById("btn-wishlist");

garmentsBtn.addEventListener("click", async function () {
    window.location.href = "garments.html";
});

wishlistBtn.addEventListener("click", () => {
    window.location.href = "wishlist.html";
});