
function initOpenLayersMap() {

    if ($('#mapid').length > 0) {
        var center = {Lat: 48.93, Lng: 32.12};
        zoom = 7;

        var map = L.map('mapid', {
            center: new L.LatLng(center.Lat, center.Lng),
            zoom: zoom,
            layers: []
        });
        addData(map);

        $(window).on("resize", function () {  //set full height of map
         $("#mapid").height($(window).height() - 70).width($(window).width() - 20);
         map.invalidateSize();
         }).trigger("resize");
    }
}

function addData(map) {

    var osmTitleLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 20,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    });

    var yandexTitleLayer = L.tileLayer('http://vec{s}.maps.yandex.net/tiles?l=map&v=4.55.2&z={z}&x={x}&y={y}&scale=2&lang=ru_RU', {
        subdomains: ['01', '02', '03', '04'],
        maxZoom: 20,
        attribution: '<a http="yandex.ru" target="_blank">Яндекс</a>',
        reuseTiles: true,
        updateWhenIdle: false
    });

    var clouds = L.OWM.clouds({showLegend: true, opacity: 0.5});
    var cloudscls = L.OWM.cloudsClassic({showLegend: true, opacity: 0.5});
    var precipitation = L.OWM.precipitation({showLegend: true, opacity: 0.5});
    var precipitationcls = L.OWM.precipitationClassic({showLegend: true, opacity: 0.5});
    var rain = L.OWM.rain({showLegend: true, opacity: 0.5});
    var raincls = L.OWM.rainClassic({showLegend: true, opacity: 0.5});
    var snow = L.OWM.snow({showLegend: true, opacity: 0.5});
    var pressure = L.OWM.pressure({showLegend: true, opacity: 0.5});
    var pressurecntr = L.OWM.pressureContour({showLegend: true, opacity: 0.5});
    var temp = L.OWM.temperature({showLegend: true, opacity: 0.5});
    var wind = L.OWM.wind({showLegend: true, opacity: 0.5});

    if (typeof markersi !== 'undefined') {
     markersi.clearLayers();
     }
    L.Icon.Default.imagePath = '/static/mbr/img/markers/'
    var path = L.Icon.Default.imagePath;
    var marker_storm = L.icon({
            iconUrl: path + 'marker-storm-small-icon.png',
            shadowUrl: path + 'marker-shadow-small-icon.png',
        }),
        marker_avia = L.icon({
            iconUrl: path + 'marker-avia-small-icon.png',
            shadowUrl: path + 'marker-shadow-small-icon.png',
            iconAnchor:   [-5, 0],
            //shadowAnchor: [4, 62],
            popupAnchor:  [15, 0]

        });

    var baseMaps = {
        "Yandex map layer" : yandexTitleLayer.addTo(map),
        "Open street layer": osmTitleLayer.addTo(map)
    };

    var overlayMaps = {
        "VOA data": addVoaDataToMap(map),
        "STORM WAREP data": addWarepStormDataLayerToMap(warepstormlist, marker_storm, map),
        "AVIA WAREP data": addWarepAviaDataLayerToMap(warepavialist, marker_avia, map),
        "Clouds":clouds.addTo(map)
        /*"Clouds classic":cloudscls.addTo(map),
        "Precipitation":precipitation.addTo(map),
        "Precipitation classic":precipitationcls.addTo(map),
        "Rain": rain.addTo(map),
        "Rain classic": raincls.addTo(map),
        "Snow": snow.addTo(map),
        "Pressure": pressure.addTo(map),
        "Pressure contour": pressurecntr.addTo(map),
        "Temperature": temp.addTo(map),
        "Wind": wind.addTo(map)*/

    };

    controlLayers = L.control.layers(baseMaps, overlayMaps).addTo(map);
}

function addVoaDataToMap(map) {
    var geojsonMarkerOptions = {
        radius: 8,
        fillColor: "#5237de",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };

   var gostomel = L.circleMarker([50.59, 30.21], geojsonMarkerOptions).bindPopup('Gostomel'),
        baryshivka = L.circleMarker([50.35, 31.34], geojsonMarkerOptions).bindPopup('Baryshivka'),
        btserkva = L.circleMarker([49.78, 30.18], geojsonMarkerOptions).bindPopup('Bila Tserkva'),
        oster = L.circleMarker([50.95, 30.95], geojsonMarkerOptions).bindPopup('Oster');

   var voalocation = L.layerGroup([gostomel, baryshivka, btserkva, oster]);

   return voalocation
}

function addWarepStormDataLayerToMap(warepdata, map_marker, map) {

    var geojsonMarkerOptions = {
        radius: 6,
        fillColor: "#a4debf",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };
    return L.geoJson(warepdata, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {icon: eval(map_marker)});
        },
        onEachFeature: function (feature, layer) {
            var myLayer = layer;
            myLayer.bindPopup(feature.properties.popupContent);
            return myLayer;
        }
    }).addTo(map);
}

function addWarepAviaDataLayerToMap(warepdata, map_marker, map) {

    var geojsonMarkerOptions = {
        radius: 6,
        fillColor: "#a4debf",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };
    return L.geoJson(warepdata, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {icon: eval(map_marker)});
        },
        onEachFeature: function (feature, layer) {
            var myLayer = layer;
            myLayer.bindPopup(feature.properties.popupContent);
            return myLayer;
        }
    }).addTo(map);
}

function addWarepAllDataLayerToMap(warepdata, map_marker, map) {

    var geojsonMarkerOptions = {
        radius: 6,
        fillColor: "#a4debf",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };
    return L.geoJson(warepdata, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {icon: eval(map_marker)});
        },
        onEachFeature: function (feature, layer) {
            var myLayer = layer;
            myLayer.bindPopup(feature.properties.popupContent);
            return myLayer;
        }
    }).addTo(map);
}

function addWarepAllDataToMap(warepdata, map) {

    var geojsonMarkerOptions = {
        radius: 6,
        fillColor: "#a4debf",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };

    L.geoJson(warepdata, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng);
        }
    }).addTo(map);

    function onEachFeature(feature, layer) {
        if (feature.properties && feature.properties.popupContent) {
            layer.bindPopup(feature.properties.popupContent);
        }
    }

    L.geoJSON(warepdata, {
        onEachFeature: onEachFeature
    }).addTo(map);
}

function addKmlRadarDataLayerToMap(map) {
    var kmlLayer = new L.KML("PH_2017-02-03_1737.kml", {async: true});
}