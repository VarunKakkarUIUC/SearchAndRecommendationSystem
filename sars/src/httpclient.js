class HttpClient {
	
 get (url, target) {
		  return new Promise(function(resolve, reject) {
			    var req = new XMLHttpRequest();
			    req.open('GET', url);
			    if (target) {
			    	req.setRequestHeader("Target-URL", encodeURI(target));
			    }
			    req.onload = function() {
			      if (req.status === 200) {
			        resolve(req.response);
			      }
			      else {
			        reject(Error(req.statusText));
			      }
			    };

			    req.onerror = function() {
			      reject(Error("Network_Error"));
			    };

			    req.send();
		  });
	}
}


const httpClient = new HttpClient();
export {
    httpClient as
    default
};
