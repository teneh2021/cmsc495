window.writeln("hello");
alert("Just trying");
console.log("hello");

function FileHelper() {
    FileHelper.readStringFromFileAtPath = function (pathOfFileToReadFrom) {
        var request = new XMLHttpRequest();
        request.open("GET", pathOfFileToReadFrom, false);
        request.send(null);
        var returnValue = request.responseText;

        return returnValue;
    }
}


var text = FileHelper.readStringFromFileAtPath("template/health_facts.txt");

var arr = text.split("\n");
document.write(arr.toString);
document.getElementById("output1").innerHTML = text;