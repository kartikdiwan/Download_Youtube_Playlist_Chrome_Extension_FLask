function send_playlist()
{
    var label = document.createElement("label");
    label.innerHTML = "Downloading...";
    document.getElementById("downloading").appendChild(label);
    chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs){
        $.ajax({
            headers: { 
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
            'type': 'POST',
            'url': "http://localhost:8008/",
            'data': JSON.stringify(tabs[0].url),
            'dataType': 'json',
            success: function(recieved_data){
                var label = document.createElement("label");
                label.innerHTML = recieved_data;
                document.getElementById("downloads").appendChild(label);
            }
        });
    });
    
}
window.addEventListener("load", send_playlist());