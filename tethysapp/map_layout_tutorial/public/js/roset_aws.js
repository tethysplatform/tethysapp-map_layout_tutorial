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
    let start_date = document.getElementById("start-date").value
    let end_date = document.getElementById("end-date").value
    let state_id = document.getElementById("state_id").value
    let model_id = document.getElementById("model_id").value
    // dropdwon id --> value
    var data = new URLSearchParams();
    data.append('method', 'update_data');
    data.append('start_date', start_date);
    data.append('end_date', end_date);
    data.append('state_id', state_id);
    data.append('model_id', model_id);
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
     });

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