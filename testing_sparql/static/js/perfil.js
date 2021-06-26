var listaInformacion = []

$(document).ready(function () {
    var cantante = document.getElementById("cantante").value.replace(/\_+/g, ' ');
    listaInformacion = JSON.parse(document.getElementById("informacion-cantante").value);
    $("#mostar-info-cantante").empty();
    if (listaInformacion.length == 0){
        $("#mostar-info-cantante").append('<p>No se ha encontrado información sobre '+cantante+'</p>');
    } else {
        $("#mostar-info-cantante").append('<h1>'+cantante+'</h1>');
        for (info of listaInformacion) {
            $("#mostar-info-cantante").append('<p>'+info+'</p>');
        }
    }
});

