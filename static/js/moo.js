
/* Configuration */
var API_URL = "/api/";
var TIMEOUT = 3000;
var MIN_ZINDEX = 101;
/* End of Configuration */


/* initiate the main map element */
function map_create() {
    return new ol.Map({
        layers: [new ol.layer.Tile({ source: new ol.source.OSM() })],
        target: 'map',
        view: new ol.View({
            center: [0,0],
            zoom: 2,
            minZoom: 2,
        })
    });
}


/* get location of user from browser api */
function geolocation(map) {
    /* try to get location from user */
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var new_center = geo_transform([position.coords.longitude, position.coords.latitude]);
            map.getView().setCenter(new_center);
            create_marker(map, [position.coords.longitude, position.coords.latitude],
                                "You're here !",
                                "point_marker");
        }, function(error_msg){
            // if user reject geo tagging or browser not able to get-it
            console.log('geo_default', error_msg);
            var new_center = geo_transform(coords_rennes);
            map.getView().setCenter(new_center);
        });
    } else {
        error('not supported');
    }
}


/* transform GPS coords to a map projection */
function geo_transform(coords) {
    return ol.proj.transform(coords, 'EPSG:4326', 'EPSG:3857');
}


/* create a std marker point */
function create_marker(map, coords, title, css) {
    var pos = geo_transform(coords);
    var d = $('<div class="'+css+'" title="'+title+'"></div>');
    d.tooltip();
    var marker = new ol.Overlay({
        position: pos,
        positioning: 'center-center',
        element: d.get(0),
        stopEvent: false,
        insertFirst: false
    });
    map.addOverlay(marker);
    return d;
}


/* get infos to create a new moo pointer */
function gen_moo_point(map, moo) {
    // create point on map
    var coords = [parseFloat(moo.longitude),
                  parseFloat(moo.latitude)];
    var point = create_marker(map,
                              coords,
                              moo.username,
                              "marker "+ moo.animal +" inclinate");
    if (moo.id > last_id) {
        last_id = moo.id;
    }
}


var last_id = null; // shared pointer to the last moo id


/* get new moo since the last_id */
function get_new_moos(map) {
    var uri = API_URL +  "moo/get_lasts"
    if (last_id) { // add ?timestamp= to the request if not first one
        uri += "?id="+last_id;
    }
    // proceed to xhr request
    $.getJSON(uri, function(data) {
        data.moos.reverse();
        // if everything works on request, create moo points
        $.each(data.moos, function(i) {
            gen_moo_point(map, data.moos[i]);
        });
    })
    .fail(function() {
        // 404, 500 etc.
        console.log("Error during request");
    })
}



/* init page */
var map = null;
function init() {
    map = map_create();
    geolocation(map);

    $(window).scroll(function () {
        if ($(window).scrollTop() == 0) {
            $('#btn-show-about-from-index').attr('href', "#about");
            $('#btn-show-about-from-index').attr('title', "About this page");  
        } else if ($(window).height() + $(window).scrollTop()
                    == $(document).height()) {
            $('#btn-show-about-from-index').attr('href', "#");
            $('#btn-show-about-from-index').attr('title', "Show the map");
        }
        console.log($(window).scrollTop());
    });
    
    get_new_moos(map);
    /* start moo getting process */
    var intervalometer = setInterval(function() { get_new_moos(map)}, TIMEOUT);
}

$(document).ready(function(){ init(); });
