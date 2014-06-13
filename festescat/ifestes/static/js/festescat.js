function showAddForm() {
    document.getElementById("LlistaElems").setAttribute("class","col-md-6");
    document.getElementById("AddForm").setAttribute("class","col-md-6");
}

function showReviewForm() {
    document.getElementById("id_rating").parentNode.parentNode.setAttribute("class","hidden");
    document.getElementById("id_user").parentNode.parentNode.setAttribute("class","hidden");
    document.getElementById("id_festa").parentNode.parentNode.setAttribute("class","hidden");
    document.getElementById("createReview").setAttribute("class","patata");
}

function hiddenReviewForm() {
    document.getElementById("createReview").setAttribute("class","hidden");
}

function mostrarPuntuacio(valor){
    $('#rating').text(valor);
}

function puntuar(rating, user, festa){
    document.getElementById('id_rating').value = rating;
    document.getElementById('id_user').value = user;
    document.getElementById('id_festa').value = festa;
    showReviewForm();
}