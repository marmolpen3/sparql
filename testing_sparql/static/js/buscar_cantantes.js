var listaCantantes = []


$(document).ready(function () {
    listaCantantes = JSON.parse(document.getElementById("lista-cantantes").value);
    $("#cantantes").empty();
    if (listaCantantes.length == 0){
        $("#cantantes").append("<p class='text-light h6 mt-5'>We could not find this artist. Please enter another artist's name.</p>");
    } else {
        for (cantante of listaCantantes) {
            $("#cantantes").append('<li class="list-group-item"><a href="/cantante/'+cantante.replace(/\s+/g, '_')+'/" class="text-decoration-none">'+cantante+'</a></li>');
        }
    }
});
