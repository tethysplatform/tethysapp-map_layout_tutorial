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
    let ol_map = TETHYS_MAP_VIEW.getMap();
    
    // dropdwon id --> value
    var data = new URLSearchParams();
    data.append('method', 'update_data');
    data.append('start_date', start_date);
    data.append('end_date', end_date);
    data.append('state_id', state_value);
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


        stations_geojson['crs']['properties']['name'] = 'EPSG:3857'
        const vectorSource = new ol.source.Vector({
            features: new ol.format.GeoJSON().readFeatures(stations_geojson),
          });
        var vectorLayer = new ol.layer.Vector({
            source: vectorSource,
            // style: style_custom
        });
        ol_map.addLayer(vectorLayer);
        //change the content of the popup
        TETHYS_MAP_VIEW.mapClicked(function(coords) {
            let popup_content = document.querySelector("#properties-popup-content");
            let lat_lon = ol.proj.transform(coords, 'EPSG:3857', 'EPSG:4326');
            let rounded_lat = Math.round(lat_lon[1] * 1000000) / 1000000;
            let rounded_lon = Math.round(lat_lon[0] * 1000000) / 1000000;
            popup_content.innerHTML = `<b>Coordinates:</b><p>${rounded_lat}, ${rounded_lon}</p>`;
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
        console.log(MAP_LAYOUT)
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