var request = require('request');

const options = {
url: 'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey=<apiKeySecret>',
method: 'POST',
json: { 
		"siteUrl":"https://lehi.dev", 
		"urlList":
		[ 
			"https://motivational.lehi.dev/",
			"https://www.lehi.dev/",
			"https://www.lehi.dev/home",
			"https://www.lehi.dev/about",
			"https://www.lehi.dev/publications",
			"https://tutorials.lehi.dev/"
		] 
	  }
};

request(options, (err, resp, body) => {
console.log(body);
});

