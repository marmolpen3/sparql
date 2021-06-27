var listaCantantes = []


$(document).ready(function () {
    listaCantantes = JSON.parse(document.getElementById("lista-cantantes").value);
    $("#cantantes").empty();
    if (listaCantantes.length == 0){
        $("#cantantes").append('<p>No se han encontrado cantantes con ese nombre</p>');
    } else {
        for (cantante of listaCantantes) {
            $("#cantantes").append('<li class="list-group-item"><a href="/cantante/'+cantante.replace(/\s+/g, '_')+'/" class="text-decoration-none">'+cantante+'</a></li>');
        }
    }
});
