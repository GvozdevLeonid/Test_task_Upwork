var myTimer = 1000

function Update() {
    window.setTimeout(Update, myTimer);
    UpdateStatuses();
}

function UpdateInterval() {
    myTimer = document.getElementById("Timer").value;
}


function UpdateStatuses() {
    var elements = document.getElementsByTagName("li");

    var data = {}
    for (var e of elements) {
        if(e.children[0].checked) data[e.getAttribute("id")] = e.innerText
    }

    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        url: "/update/",
        cache: false,
        data: data,
    }).done(function (response) {
        for (var item of response) {
            var element = document.getElementById(item.id);
            if(item.status == "ok") element.setAttribute("class", "list-group-item list-group-item-success");
            else if (item.status == "bad") element.setAttribute("class", "list-group-item list-group-item-danger");
            else element.setAttribute("class", "list-group-item list-group-item-warning");
        }
    });

}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


window.setTimeout(Update, myTimer);