$(document).ready(function () {
    var cantante = document.getElementById("cantante").value.replace(/\_+/g, ' ');
    var datos = JSON.parse(document.getElementById("informacion-cantante").value);
    $("#mostar-info-cantante").empty();
    console.log(datos);
    $("#mostar-info-cantante").append('<h1>'+cantante+'</h1>');
    $("#mas-info").append('<h4>More information about '+cantante+'</h4>');
    Object.entries(datos).forEach(([k,v]) => {
        if (k == 'info')
        $("#mostar-info-cantante").append('<p class="text-start mt-3">'+v+'</p>');
        if (k == 'nombreGenero') {
            var generos = "";
            for (genero of v) {
                if (genero != "")
                    generos = generos + genero + ", ";
            }
            generos = generos.substring(0,generos.length-2);
            $("#mostar-info-cantante").append('<h5>'+generos+'</h5>');
        }
        if (k == 'ocupacion') {
            var ocupaciones = "";
            for (ocupacion of v) {
                if (ocupacion != "")
                    ocupaciones = ocupaciones + ocupacion + ", ";
            }
            ocupaciones = ocupaciones.substring(0,ocupaciones.length-2);
            $("#mas-info").append('<h6>Occupation(s): '+ocupaciones+'</h6>');
        }

        if (k == 'nombreCancion') {
            var canciones = "";
            for (cancion of v) {
                if (cancion != "")
                canciones = canciones + cancion + ", ";
            }
            canciones = canciones.substring(0,canciones.length-2);
            $("#mas-info").append('<p class="text-start mt-3">Popular songs: <em>'+canciones+'</em></p>');
        }

    });


    // if (datos.length == 0){
    //     $("#mostar-info-cantante").append('<p>No se ha encontrado información sobre '+cantante+'</p>');
    // } else {
    //     $("#mostar-info-cantante").append('<h1>'+cantante+'</h1>');
    //     for (info of datos) {
    //         $("#mostar-info-cantante").append('<p>'+info+'</p>');
    //     }
    // }
});

