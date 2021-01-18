// function to download the file 
function getCSV() {
    let xhr = new XMLHttpRequest();
    let url = "/app/download_file";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            downloadCSV(this.responseText);
        }
    };
    xhr.send();
}


// this function is use to delete file that is not important, from server side
function deleteFile() {
    let xhr = new XMLHttpRequest();
    let url = "/app/delete_file";
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            location.replace(JSON.parse(this.responseText)['redirect']);
        }
    };
    xhr.send();
}


// this function send request to server to get predicted csv file and file get downloaded
function downloadCSV(file) {
    let blob = new Blob([file]);
    let url = window.URL.createObjectURL(blob);

    let link = document.createElement('a');
    document.getElementById("downloadbutton").appendChild(link);
    link.href = url;
    link.download = "file.csv";
    link.click();

    setTimeout(() => {
        window.URL.revokeObjectURL(url);
        link.remove();
    }, 1);

    deleteFile();
}


// function to display table 
function onLoadPage() {
    let url = "/app/get_table";
    $.get(url, function (data) {
        if (data) {
            document.getElementById("tables").innerHTML = data;
        }
    });
}
window.onload = onLoadPage;