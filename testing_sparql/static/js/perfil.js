$(document).ready(function () {
    var cantante = document.getElementById("cantante").value.replace(/\_+/g, ' ');
    var imgCantante = document.getElementById("img-cantante").value;
    var datos = JSON.parse(document.getElementById("informacion-cantante").value);
    $("#mostar-info-cantante").empty();
    $("#mostar-info-cantante").append('<h1 class="my-2">'+cantante+'</h1>');
    $("#mostar-info-cantante").append('<img src="'+imgCantante+'" class="img-fluid img-thumbnail w-50 my-2"></img>');
    if(datos['nombreGenero'].length == 0 && datos['info'] == null){
        $("#mostar-info-cantante").append('<p class="mt-3">We could not find any information about this artist. Sorry :(</p>');
    }
    $("#mas-info").append('<h4 class="my-2">More information about '+cantante+'</h4>');
    Object.entries(datos).forEach(([k,v]) => {
        if (k == 'info')
        $("#mostar-info-cantante").append('<p class="text-start mt-4">'+v+'</p>');
        if (k == 'nombreGenero') {
            var generos = "";
            for (genero of v) {
                if (genero != "")
                    generos = generos + genero + ", ";
            }
            generos = generos.substring(0,generos.length-2);
            $("#mostar-info-cantante").append('<h5>'+generos+'</h5>');
        }
        if (k == 'nombreOcupacion') {
            if (v.length != 0){
                $("#mas-info-card").removeClass("d-none");
                var ocupaciones = "";
                for (ocupacion of v) {
                    if (ocupacion != "")
                        ocupaciones = ocupaciones + ocupacion + ", ";
                }
                ocupaciones = ocupaciones.substring(0,ocupaciones.length-2);
                $("#mas-info").append('<h6>Occupation(s): '+ocupaciones+'</h6>');
            }
        }

        if (k == 'pagWeb') {
            if (v != ""){
                $("#mas-info-card").removeClass("d-none");
                $("#mas-info").append('<p class="text-start mt-4"><u>Web page</u>: <a class="text-decoration-none" href="'+v+'">'+v+'</a></p>');
            }
        }

        if (k == 'nominaciones'){
            Object.entries(v).forEach(([k,v]) => {
                if (k == 'nombre' && v.length != 0 ){
                    $("#mas-info-card").removeClass("d-none");
                    $("#mas-info").append('<p class="text-start my-4"><u>Nomination(s)</u>: <em>'+v+'</em></p>');
                }
                if(k == 'info' && v.length != 0 ){
                    $("#mas-info-card").removeClass("d-none");
                    $("#mas-info").append('<button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-info" aria-expanded="false" aria-controls="collapse-info">Show more about these awards</button>');
                    $("#mas-info").append('<div class="collapse" id="collapse-info"><div id="awards-info" class="card card-body mt-3"></div></div>');
                    for (i of v) {
                        $("#awards-info").append('<p class="text-start mb-4"><i class="bi bi-arrow-right-circle"></i> '+i+'</p>');
                    }
                }
            });
        }

        if (k == 'nombreCancion') {
            if (v.length != 0){
                $("#mas-info-card").removeClass("d-none");
                var canciones = "";
                for (cancion of v) {
                    if (cancion != "")
                    canciones = canciones + cancion + ", ";
                }
                canciones = canciones.substring(0,canciones.length-2);
                $("#mas-info").append('<p class="text-start mt-4"><u>Popular songs</u>: <em>'+canciones+'</em></p>');
            }
        }

    });
});

