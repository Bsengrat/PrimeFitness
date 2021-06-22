
document.getElementById('sub').onclick = function() {
    var disabled = document.getElementById("name").disabled;
    if (disabled) {
        document.getElementById("name").disabled = false;
        document.getElementById("name2").disabled = false;
        document.getElementById("name3").disabled = false;
    }
    else {
        document.getElementById("name").disabled = true;
        document.getElementById("name2").disabled = true;
        document.getElementById("name3").disabled = true;
    }
}
