// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
let csrftoken = getCookie('csrftoken');

//const image = new CircleStyle({
  //  radius: 5,
    //fill: null,
    //stroke: new Stroke({color: 'red', width: 1}),
  //});
  
  //const styles = {
    //'Point': new Style({
      //  radius: 5,
        //fill: 'red',
     //   stroke: new Stroke({color: 'red', width: 1}),
   // }),
  //'MultiLineString': new Style({
    //stroke: new Stroke({
      //color: 'green',
      //width: 1,
    //}),
  //}),
//};

// let start_date = document.getElementById("start-date").value
// let end_date = document.getElementById("end-date").value

// var data = new URLSearchParams();
// data.append('method', 'test_rest_api');
// data.append('start_date', start_date);
// data.append('end_date', end_date);
// data.append('state_id', 'random_id');


// make an onchange function here 
document.getElementById("btn-id").addEventListener('click',function(){
    // remove state if is here //

    let start_date = document.getElementById("start-date").value
    let end_date = document.getElementById("end-date").value
    let state_value = document.getElementById("select_state").value
    let model_name = document.getElementById("select_model").value
    let ol_map = TETHYS_MAP_VIEW.getMap();
    
    // dropdwon id --> value
    var data = new URLSearchParams();
    data.append('method', 'update_data');
    data.append('start_date', start_date);
    data.append('end_date', end_date);
    data.append('state_id', state_value);
    data.append('model_id', model_name);
    //make the function here
    fetch(".", {
        method: 'POST',
        headers: {
           "Content-Type": "application/x-www-form-urlencoded",
           "X-CSRFToken": csrftoken 
        },
        body: data
     }).then((response) => response.json()).then((data) => {

     // Do something magical with your data :)

        let stations_geojson = JSON.parse(data['stations_geojson']);
        stations_geojson['features'] = stations_geojson['features'].map(station => {
            return {
                type: "Point",
                geometry: {
                    type: "Point",
                    coordinates: ol.proj.transform(
                        [
                            parseFloat(station['geometry']['coordinates'][0]),
                            parseFloat(station['geometry']['coordinates'][1])
                        ],
                        "EPSG:4326",
                        "EPSG:3857"
                    )
                },
                properties: station['properties'],
                type: station['type'],
            }
        })

        console.log(stations_geojson['crs'])
        stations_geojson['crs']['properties']['name'] = 'EPSG:3857'

        // add the flowlines
        //let flowpaths_geojson = JSON.parse(data['flowpaths_geojson']);
        //flowpaths_geojson['features'] = flowpaths_geojson['features'].map(flowpaths => {
          //  return {
            //    type: "MultiLineString",
              //  geometry: {
               //     type: "MultiLineString",
                //    coordinates: ol.proj.transform(
                 //       [
                 //           parseFloat(flowpaths['geometry']['coordinates'][0]),
                   //         parseFloat(flowpaths['geometry']['coordinates'][1])
                    //    ],
                    //    "EPSG:4326",
                    //    "EPSG:3857"
                   // )
               // },
               // properties: flowpaths['properties'],
              //  type: flowpaths['type'],
           // }
        //})



        //flowpaths['crs']['properties']['name'] = 'EPSG:3857'
         //import {Circle as CircleStyle, Fill, Stroke, Style} from 'ol/style.js';

        //const vectorSource = new ol.source.Vector({
        //    features: new ol.format.GeoJSON().readFeatures(flowpaths_geojson),
        //  });
        //var vectorLayer = new ol.layer.Vector({
        //    source: vectorSource,
            // style: style_custom
       // });



       // functions to change item colors
       //const image = new ol.style.Circle({
       // /radius: 5,
        //fill: null,
        //stroke: new ol.style.Stroke({color: 'red', width: 1}),
      //});
      
        const styles = {
        'Point': new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: 'red',
                width: 2,
            }),
            fill: new ol.style.Fill({
                color: 'rgba(255,0,0,0.2)',
            }),
            }),
        'LineString': new ol.style.Style({
            stroke: new ol.style.Stroke({
            color: 'green',
            width: 1,
            }),
        }),
        'MultiLineString': new ol.style.Style({
            stroke: new ol.style.Stroke({
            color: 'green',
            width: 1,
            }),
        }),
        'MultiPolygon': new ol.style.Style({
            stroke: new ol.style.Stroke({
            color: 'yellow',
            width: 1,
            }),
            fill: new ol.style.Fill({
            color: 'rgba(255, 255, 0, 0.1)',
            }),
        }),
        'Polygon': new ol.style.Style({
            stroke: new ol.style.Stroke({
            color: 'blue',
            lineDash: [4],
            width: 3,
            }),
            fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.1)',
            }),
        }),
        'Circle': new ol.style.Style({
            stroke: new ol.style.Stroke({
            color: 'red',
            width: 2,
            }),
            fill: new ol.style.Fill({
            color: 'rgba(255,0,0,0.2)',
            }),
        }),
        };

        const styleFunction = function (features) {
            return styles[features.getGeometry().getType()];
        };
        const vectorSource = new ol.source.Vector({
            features: new ol.format.GeoJSON().readFeatures(stations_geojson),
          });
        var vectorLayer = new ol.layer.Vector({
            source: vectorSource,
           // style: styleFunction // hash this line out if fails
            });


        ol_map.addLayer(vectorLayer);
        //change the content of the popup
        TETHYS_MAP_VIEW.mapClicked(function(coords) {
            let popup_content = document.querySelector("#properties-popup-content");
            let lat_lon = ol.proj.transform(coords, 'EPSG:3857', 'EPSG:4326');
            let rounded_lat = Math.round(lat_lon[1] * 1000000) / 1000000;
            let rounded_lon = Math.round(lat_lon[0] * 1000000) / 1000000;
            console.log(ol.style)
 


            let sitelocation = 'Cool River';
            let nwisid = '00000000';
            let model_reach_id = '11111111';
            popup_content.innerHTML = `<b>Site name:</b><p>${sitelocation}<p>
                                        <b>NWIS id:</b><p>${nwisid}<p>
                                        <b>Model reach id:</b><p>${model_reach_id}<p>
                                        <b>Coordinates:</b><p>${rounded_lat}, ${rounded_lon}</p>`;

            MAP_LAYOUT.show_plot()
            // https://docs.tethysplatform.org/en/stable/tethys_sdk/layouts/map_layout.html#map-layout-js-get-plot
            // var data = new URLSearchParams();
            // data.append('method', 'get_plot');

            // fetch(".", {
            //     method: 'POST',
            //     headers: {
            //        "Content-Type": "application/x-www-form-urlencoded",
            //        "X-CSRFToken": csrftoken 
            //     },
            //     body: data
            //  }).then((response) => response.json()).then((data) => {

            //    you will call MAP_LAYOUT.update_plot()
            // })
        
        });
        //console.log(MAP_LAYOUT)
     });
// 4326
})

// fetch(".", {
//    method: 'POST',
//    headers: {
//       "Content-Type": "application/x-www-form-urlencoded",
//       "X-CSRFToken": csrftoken 
//    },
//    body: data
// }).then((response) => response.json()).then((data) => {
// // Do something magical with your data :)
// });
