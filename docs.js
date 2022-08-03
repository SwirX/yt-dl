var selectedFile = "";

var main_py_code = "";

function print(value) {
    console.log(value);
};

function onClick(id) {
    print('clicked')
    print(id)
        if (id.includes(".py") == true){
            print("python");
            var code = document.getElementById('previewpy');
            code.style.display = "none"
        }
        else if (id.includes(".json") == true){
            print('json');
            var code = document.getElementById('previewjson');}
        else if (id.includes(".tcl") == true){
            print('tcl');
            var code = document.getElementById('previewtcl');}
        else if (id.includes(".txt") == true){
            print('text');
            var code = document.getElementById('previewtxt');}
        else if (id.includes(".bat") == true){
            print('batch');
            var code = document.getElementById("previewbat");}
}

var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}