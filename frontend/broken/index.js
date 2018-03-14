import $ from "jquery";
import Cropper from "cropperjs"
// import "cropper.css"

var image;
var _URL = window.URL || window.webkitURL;

const file1 = document.getElementById("file")


function postImgToServer(image) {
    const img = new FormData();
    img.append('type', 'file');
    img.append('image', image);
    img.append('name', 'content_img');
    console.log('IMG ', image)
    console.log('IMG ', img)
    console.log('s ', image.src)
    console.log('d ', img.src)

    fetch("//192.168.5.165:8080/upload", {
        headers: {
            'Accept': 'application/json, application/xml, text/plain, text/html, *.*',
            'Content-Type': 'multipart/form-data'
        },
        mode:'no-cors',
        method: 'post',
        body: img
    })
        .catch(err => console.log("ERROR", err))
        .then(data => console.log('done sending'))
}

// file1.addEventListener('change', function (e) {
//     let file;
//     let src;
// })

function fileUpload() {

}

$("#file").change(function (e) {
    let file;
    let src;
    if ((file = this.files[0])) {
	image = new Image();
        image.src = _URL.createObjectURL(file);

        image.onload = function () {
            src = this.src;
            $('#uploadPreview').html('<img src="' + src + '"></div>');

            postImgToServer(file)
            e.preventDefault();
        }
    }
})
