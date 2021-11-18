// function to copy text 
function copyToClipboard(elementId) {
    let aux = document.createElement("input");
    aux.setAttribute("value", document.getElementById(elementId).innerHTML);
    document.body.appendChild(aux);
    aux.select();
    document.execCommand("copy");
    document.body.removeChild(aux);
    document.getElementById("output").innerHTML = "Copied.";
    setTimeout(clear, 1000);
}

// function to capitalize options 
function capitalize(word) {
    return word[0].toUpperCase() + word.slice(1).toLowerCase();
}

// function to clear output screen
function clear() {
    document.getElementById("output").innerHTML = "";
}

// function to read value input in html 
function formInput() {
    let age = document.getElementById("input1").value;
    age == "" ? age = parseFloat("40") : parseFloat(age);
    let job = document.getElementById("input2").value;
    let marital = document.getElementById("input3").value;
    let education = document.getElementById("input4").value;
    let default1 = document.getElementById("input5").value;
    let contact = document.getElementById("input6").value;
    let month = document.getElementById("input7").value;
    let week = document.getElementById("input8").value;
    let duration = document.getElementById("input9").value;
    duration == "" ? duration = parseFloat("999") : parseFloat(duration);
    let campaign = document.getElementById("input10").value;
    campaign == "" ? campaign = parseFloat("2.57") : parseFloat(campaign);
    let pday = document.getElementById("input11").value;
    pday == "" ? pday = parseFloat("962.47") : parseFloat(pday);
    let previous = document.getElementById("input12").value;
    previous == "" ? previous = parseFloat("0.173") : parseFloat(previous);
    let poutcome = document.getElementById("input13").value;
    let empVar = document.getElementById("input14").value;
    empVar == "" ? empVar = parseFloat("0.0818") : parseFloat(empVar);
    let consPrice = document.getElementById("input15").value;
    consPrice == "" ? consPrice = parseFloat("93.575") : parseFloat(consPrice);
    let consConf = document.getElementById("input16").value;
    consConf == "" ? consConf = parseFloat("-40.502") : parseFloat(consConf);
    
    return new Array(age, duration, campaign, pday, previous, empVar, consPrice, consConf,
        job, marital, default1, contact, month, week, education, poutcome);
}

// function to show file name 
function showFileName() {
    let fileName = document.getElementById("button1").files[0].name;
    document.getElementById("output").innerHTML = "Selected file is " + fileName;
    setTimeout(clear, 4000);
    document.getElementById("button1").disabled = "true";
}


// function to change submit button function when file is uploaded
function changeSumitbuttonFunction() {
    document.getElementById("submitbutton").onclick = function () { postToServer(forFileSubmit()); };
}

// function to pass formData to posttoserver 
function forFileSubmit() {
    let data = new FormData();
    let file = document.getElementById("button1").files[0];
    if (file.name.endsWith('.csv')) {
        data.append('file', file);
        data.append('file_name', file.name);
    }
    else if (file.name.endsWith('.xlsx')) {
        data.append('file', file);
        data.append('file_name', file.name);
    }
    else {
        data = null;
        document.getElementById("output").innerHTML = "Please Enter Proper file.";
    }
    document.getElementById("button1").disabled = "";
    document.getElementById("submitbutton").onclick = function () { postToServer(formInput()); };
    return data;
}

// function to display data to output screen 
function displayOutput(responseStr) {
    let jsonData;
    try {
        jsonData = JSON.parse(responseStr);
        if (jsonData["estimate_val"] == '0') {
            document.getElementById("output").innerHTML = "Predicted value is 0.<br>Client will Not subscribe to your bank.";
            setTimeout(clear, 4000);
        }
        else {
            document.getElementById("output").innerHTML = "Predicted value is 1.<br>Client will subscribe to your bank.";
            setTimeout(clear, 4000);
        }
    }
    catch (err) {
        document.getElementById("output").innerHTML = err.message;
        setTimeout(clear, 4000);
    }
}

// function to post data to data to server 
function postToServer(varTopost) {
    if (varTopost instanceof Array) {
        let xhr = new XMLHttpRequest();
        let url = "/predict_data";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                displayOutput(this.responseText);
            }
        };
        let data = JSON.stringify({ "data": varTopost });
        xhr.send(data);
    }
    else if (varTopost instanceof FormData) {
        let xhr = new XMLHttpRequest();
        let url = "/predict_csv";
        xhr.open('POST', url, true);
        xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
        xhr.send(varTopost);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                let varOnParse = JSON.parse(this.responseText)['redirect'];
                if (varOnParse === undefined) {
                    document.getElementById("output").innerHTML = JSON.parse(this.responseText)['error'];
                    setTimeout(clear, 4000);
                }
                else{
                    location.replace(JSON.parse(this.responseText)['redirect']);
                }
            }
        }
    }
    else {
        console.log("not working");
    }
}

// function to display option in select tag 
function onLoadPage() {
    let url = "/get_data";
    let getVar = ["job", "marital", "education", "month", "day_of_week"]
    let lstId = ["input2", "input3", "input4", "input7", "input8"]
    $.get(url, function (data) {
        if (data) {
            for (let i = 0; i < 5; i++) {
                let column = data[getVar[i]];
                for (let j in column) {
                    let opt = new Option(capitalize(column[j]));
                    $('#' + lstId[i]).append(opt);
                }
            }
        }
    });
}
window.onload = onLoadPage;