function send_playlist()
{
    var p = document.getElementById("downloading");
    p.innerHTML = "Downloading...";
    chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs){
        $(document).ready(function() {
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
                    var p = document.getElementById("downloading");
                    p.innerHTML = recieved_data;
                }
            });
        });
    });
    
}
window.addEventListener("load", send_playlist());