// Javascript for the front end
window.addEventListener("load", (event) => {

    const formClose = document.getElementById('formClose');


    formClose.addEventListener('click', function () {
      formClose.textContent = formClose.textContent === 'Add New' ? 'Close' : 'Add New';
    });
      
});
