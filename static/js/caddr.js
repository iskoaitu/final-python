document.addEventListener('DOMContentLoaded', function () {
    const deleteButton = document.querySelector('.delete-button');

    if (deleteButton) {
        deleteButton.addEventListener('click', function (event) {
            event.preventDefault();
            const confirmDelete = confirm('Are you sure you want to delete this recipe?');
            if (confirmDelete) {
                deleteButton.closest('form').submit();
            }
        });
    }
});
