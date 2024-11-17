document.addEventListener("DOMContentLoaded", () => {
    const galleryItems = document.querySelectorAll(".gallery-item");

    galleryItems.forEach(item => {
        item.addEventListener("mouseenter", () => {
            item.classList.add("hover");
        });
        item.addEventListener("mouseleave", () => {
            item.classList.remove("hover");
        });
    });
});
