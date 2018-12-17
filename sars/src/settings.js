const settings = {
	bingmapsApiUrl: "https://dev.virtualearth.net/REST/v1/Locations/{{point}}?includeEntityTypes=Address&key={{key}}",
	bingmapsApiKey: "AqwSSw6YyV-n2OjGf8nHvNHCprXR8YFGWhQPaXq4gXjZZ7Al-3xMaqY3VoXuK0VS",
	searchApiUrl: "https://sarsapi.azurewebsites.net",
	// searchApiUrl: "http://localhost:4000",
	searchApiTargetUrl: "http://13.77.179.28",
	// searchApiTargetUrl: "http://127.0.0.1:5000",
	searchUrlTemplate: "{{endpoint}}/v1/search?text={{searchtext}}&city={{searchcity}}&state={{searchstate}}"
};


export {
    settings as
    default
};

