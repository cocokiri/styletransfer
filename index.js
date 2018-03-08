import $ from "jquery";
import Cropper from "cropperjs"
// import "cropper.css"

var image;
var _URL = window.URL || window.webkitURL;

console.log(Cropper)
fetch("//192.168.5.165:8080/style.js", {
    method: 'post',
    headers: {
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    },
    body: 'foo=bar&lorem=ipsum'
})
    .then(data => console.log(data, "asdasd")
)

$("#file").change(function (e) {
    let file;
    let src;
    if ((file = this.files[0])) {
        console.log(file)
        image = new Image();
        image.onload = function () {
            src = this.src;
            image.src = _URL.createObjectURL(file);
            $('#uploadPreview').html('<img src="' + src + '"></div>');
            e.preventDefault();

            fetch("//192.168.5.165:8080/style.js", {
                method: 'post',
                body: new FormData().append('photo', image)
            })
                .catch(err => console.log("ERROR", err))
                .then(data => console.log('done sending'))


        }
        // image.src =
        image.src = _URL.createObjectURL(file);

    }
})