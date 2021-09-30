var BASE = '.'

// Step 1: Upload CSV
function uploadCSV(){
  if (document.getElementById("fileToUpload").files.length == 0) {
    alert("Please upload the file first.");
    return;
  }
  let fileUpload = document.getElementById("fileToUpload");
  let files = fileUpload.files;
  if (files[0].name.toLowerCase().lastIndexOf(".csv") == -1) {
    alert("Please upload only CSV files");
    return;
  }
  
  const fileInput = document.getElementById("fileToUpload").files[0];

  console.log("Uploading file...");
  const API_ENDPOINT = "/upload-file";
  const request = new XMLHttpRequest();
  const formData = new FormData();

  request.open("POST", API_ENDPOINT, true);
  request.onreadystatechange = () => {
    if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
      console.log(request.responseText);
      document.getElementById('checkfile').innerHTML =
      `<button class="btn btn--icon btn--large btn--success" hidden><span class="icon-check"></span></button>`
    }
  };

  formData.append("file", fileInput);
  request.send(formData);
}

// Step 2: Get recordings
function getRecordings() {
  document.getElementById('waiter').innerHTML =
    `<div class="loading-spinner flex-center" aria-label="Loading, please wait...">
        <div class="wrapper">
            <div class="wheel"></div>
        </div>
      </div>`
  fetch(BASE + '/get-recordings', {
    method: "get",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function (text) {
      return text.json();
  }).then(function (body) {
      console.log(body);
      document.getElementById('waiter').innerHTML =
      `<button class="btn btn--icon btn--large btn--success" hidden><span class="icon-check"></span></button>`
  });
}

// Step 3: Post to COLE
function postToCOLE(){
  document.getElementById('checkmark').innerHTML =
    `<div class="loading-spinner flex-center" aria-label="Loading, please wait...">
        <div class="wrapper">
            <div class="wheel"></div>
        </div>
      </div>`
  fetch(BASE + '/post-to-cole', {
    method: "get",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function (text) {
      return text.json();
  }).then(function (body) {
      console.log(body);
      document.getElementById('checkmark').innerHTML =
      `<button class="btn btn--icon btn--large btn--success" hidden><span class="icon-check"></span></button>`
  });
}

