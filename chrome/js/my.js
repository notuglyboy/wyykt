chrome.contextMenus.create({
    
    'type':'normal',
    'title':'asdasdfwsdfge',
    'contexts':['all']
});
 
//http://112.90.212.26/video.study.163.com/yooc-video/nos/flv/2017/08/29/
//start
var xhr = new XMLHttpRequest();
chrome.webRequest.onBeforeRequest.addListener(
    function(detail){
        if(detail.url.indexOf("edu-common-private") >= 0)
        {
            var title = document.getElementsByClassName("up j-up f-thide").value;
            console.log("title is " + title);
            
            console.log(detail.url);
            xhr.open("GET", "http://127.0.0.1:12346/ ", true);
            xhr.setRequestHeader('videolrc',detail.url);
            xhr.onreadystatechange = function(){console.log(this.responseText)}
            xhr.send();
        }
        if(detail.url.indexOf("video.study.163.com") >= 0
        && detail.url.indexOf("start") < 0) 
        {
            console.log(detail.url)
            xhr.open("GET", "http://127.0.0.1:12346/ ", true);
            xhr.setRequestHeader('videolrc',detail.url);
            xhr.onreadystatechange = function(){console.log(this.responseText)}
            xhr.send();
        }
        
    },
    {urls:["<all_urls>"]},
    []
)



