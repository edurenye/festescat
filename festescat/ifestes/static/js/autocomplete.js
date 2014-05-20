$(function() {
    //Autocomplete Static
    $.getJSON("/static/tipus_event.json", {}, function (tipus) {
        $("#id_tipus").autocomplete({ source: tipus });
    });
    var provincies = ["Barcelona", "Girona", "Lleida", "Tarragona"];
    $("#id_provincia").autocomplete({ source: provincies});

    //Autocomplete Dynamic
    $.getJSON("http://api.idescat.cat/emex/v1/nodes.json?tipus=com", {}, function (comarca) {
        var fitxes = comarca.fitxes;
        var v = fitxes.v;
        var com = [];
        $.each(v, function() {
                com.push(this['content']);
            });
        $("#id_comarca").autocomplete({ source: com });
    });
    $.getJSON("http://api.idescat.cat/emex/v1/nodes.json?tipus=mun", {}, function (municipi) {
        var fitxes = municipi.fitxes;
        var v = fitxes.v;
        var mun = [];
        $.each(v, function() {
                mun.push(this['content']);
            });
        $("#id_poble").autocomplete({ source: mun });
    });
});