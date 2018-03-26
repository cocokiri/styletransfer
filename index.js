
var image;
var _URL = window.URL || window.webkitURL;

const file1 = document.getElementById("file")

const container = document.getElementById('container');

let a = false;
let b = false;
let contentURL;
let styleURL;

const paramSubmit = document.getElementById('paramSubmit');

let ENDIMAGE_URL;

paramSubmit.addEventListener('mousedown', function(e){
    e.preventDefault();

    const paramForm = document.getElementById('params')

    const form_param = new FormData(paramForm);
    const URL = "http://192.168.5.165:8080/stylize";

    console.log("contentname", contentURL)
    console.log("stylename", styleURL)

    form_param.append("content_img_url", contentURL);
    form_param.append("style_img_url", styleURL);

    console.log(form_param.entries(), "entries")

    console.log(form_param, "form param");
    console.log(paramForm, " param Form");
    let xhr = new XMLHttpRequest();
    // Add any event handlers here...
    xhr.open('POST', URL, true);

    xhr.send(form_param);

    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            //console.log("generated Image URL :  " + xhr.responseText);
            ENDIMAGE_URL = xhr.responseText;
           // console.log("http://192.168.5.165:8080/static/images/results/" + ENDIMAGE_URL)
            //alert("http://192.168.5.165:8080/static/images/results/" + ENDIMAGE_URL)
            document.getElementById("endImg").setAttribute('src', "http://192.168.5.165:8080/static/images/results/" + ENDIMAGE_URL);
            e.preventDefault();

        }
    }
    return false;
})


const Submit = document.getElementById('submit');
Submit.hidden = true;


submit.addEventListener('mousedown', function(){
    const Forms = document.getElementsByTagName('form');
    console.log(Forms, "forms");

    var form_content = new FormData(Forms[0]);
    var form_style = new FormData(Forms[1]);

    const content = document.getElementById('contentImg').files[0]
    const style = document.getElementById('styleImg').files[0]
    form_content.append('content_img', content)
    form_style.append('style_img', style)

    console.log(form_content, "contentform")
    console.log(form_style, "styleform")
    var xhr1 = new XMLHttpRequest();
    var xhr2 = new XMLHttpRequest();
    // Add any event handlers here...
    xhr1.open('POST', Forms[0].getAttribute('action'), true);
    xhr2.open('POST', Forms[1].getAttribute('action'), true);

    xhr1.send(form_content);
    xhr2.send(form_style);

    xhr1.onreadystatechange = function() {
        if (xhr1.readyState == XMLHttpRequest.DONE) {
            contentURL = xhr1.responseText;
        }
    }
    xhr2.onreadystatechange = function() {
        if (xhr2.readyState == XMLHttpRequest.DONE) {
            styleURL = xhr2.responseText;

        }
    }
    return false;
})

$("#contentImg").change(function (e) {
    let file;
    let src;
    a= true;
    console.log("a ", a, "b ", b)
    if (a && b) {
        Submit.hidden = false;
    }
    if ((file = this.files[0])) {

        image = new Image();
        image.src = _URL.createObjectURL(file);

        image.onload = function () {
            src = this.src;
            $('#basePreview').html('<img src="' + src + '"></div>');
            console.log(image, " iamge")
            e.preventDefault();
        }
    }
})
$("#styleImg").change(function (e) {
    let file;
    let src;
    b =true;

    if (a && b) {
        Submit.hidden = false;
    }

    console.log(this.files, " files")
    if ((file = this.files[0])) {

        image = new Image();
        image.src = _URL.createObjectURL(file);

        image.onload = function () {
            src = this.src;
            $('#stylePreview').html('<img src="' + src + '"></div>');

            //sendData(image)
            console.log(image, " iamge")

            e.preventDefault();
        }
    }
})
