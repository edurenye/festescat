function showAddForm() {
    document.getElementById("LlistaElems").setAttribute("class","col-md-6");
    document.getElementById("AddForm").setAttribute("class","col-md-6");
}

function showReviewForm() {
    document.getElementById("createReview").setAttribute("class","patata");
}

function hiddenReviewForm() {
    document.getElementById("createReview").setAttribute("class","hidden");
}

function mostrarPuntuacio(valor){
    $('#rating').text(valor);
}

function puntuar(rating){
    showReviewForm();
}