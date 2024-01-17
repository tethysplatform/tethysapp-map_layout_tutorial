let checkCsrfSafe = function (method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

let getCookie = function (name) {
  let cookie;
  let cookies;
  let cookieValue = null;
  let i;

  if (document.cookie && document.cookie !== "") {
        cookies = document.cookie.split(";");
        for (i = 0; i < cookies.length; i += 1) {
              cookie = $.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break
              }
        }
  }
  return cookieValue;
};
function fetchData() {


  fetch(".", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: {
      method: "update-dates",
      other: 1,
      another: true
    },
  })
  .then((response) => console.log(response))
  .then((data) => {
    // Handle the response data
    console.log(data);
    // Perform actions with the received data
  })
  .catch((error) => {
    // Handle errors
    console.log(error);
  });
}
fetchData()