import httpClient from './httpclient'
import settings from './settings'

class LocationProvider {
	
	loadPosition = async () => {
	    try {
	      const position = await this.getCurrentPosition();
	      const { latitude, longitude } = position.coords;
	      let mapsurl = settings.bingmapsApiUrl.replace("{{point}}", latitude +","+ longitude).replace("{{key}}", settings.bingmapsApiKey);
	      let locationString = await httpClient.get(mapsurl);
	      let location = JSON.parse(locationString);
	      let address = location.resourceSets[0].resources[0].address; 
	      return {
	        lat: latitude,
	        long: longitude,
	        error: null,
	        address: address
	      };
	    } catch (error) {
	      console.log(error);
	      return {
	        lat: null,
	        long: null,
	        address: null,
	        error: error
	      };
	    }
  };

  getCurrentPosition = (options = {}) => {
    return new Promise((resolve, reject) => {
    	if ("geolocation" in navigator) {
	       navigator.geolocation.getCurrentPosition(resolve, reject, options);
	    } else {
	    	reject(Error("GeoLocation_Not_Supported"))
	    }
    });
  };

}


const locationProvider = new LocationProvider();
export {
    locationProvider as
    default
};
