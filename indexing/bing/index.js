var request = require('request');

const options = {
url: 'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey=<apiKeySecret>',
method: 'POST',
json: { 
		"siteUrl":"https://lehi.dev", 
		"urlList":
		[ 
			"https://motivational.lehi.dev/",
			"https://motivational.lehi.dev/2023/07/why-i-succeed.html",
			"https://motivational.lehi.dev/2023/06/love-what-you-do.html",
			"https://motivational.lehi.dev/2023/06/do-not-stop.html",
			"https://motivational.lehi.dev/2023/06/slow-and-steady-wins-race.html",
			"https://motivational.lehi.dev/2023/06/i-havent-failed.html",
			"https://motivational.lehi.dev/2023/06/the-greatest-danger.html",
			"https://motivational.lehi.dev/2023/06/secret-of-change.html",
			"https://motivational.lehi.dev/2023/06/tragedy-of-life.html",
			"https://motivational.lehi.dev/2023/06/focus-determines-your-reality.html",
			"https://motivational.lehi.dev/2023/06/the-man-of-tomorrow.html",
			"https://motivational.lehi.dev/2023/06/your-situation-is-as-powerful-as-gravity.html",
			"https://motivational.lehi.dev/2023/06/grit.html",
			"https://motivational.lehi.dev/2023/06/greatest-rewards.html",
			"https://motivational.lehi.dev/2023/06/dream-big.html",
			"https://motivational.lehi.dev/2023/06/never-too-late.html",
			"https://motivational.lehi.dev/2023/06/dealt-different-hand.html",
			"https://motivational.lehi.dev/2023/06/we-keep-moving-forward-opening-new.html",
			"https://motivational.lehi.dev/2023/06/become-man-of-value.html",
			"https://motivational.lehi.dev/2023/05/good-idea.html",
			"https://motivational.lehi.dev/2023/04/success.html",
			"https://motivational.lehi.dev/2023/04/game.html",
			"https://motivational.lehi.dev/2023/04/doing.html",
			"https://motivational.lehi.dev/2023/04/light.html",
			"https://motivational.lehi.dev/2023/04/learn.html",
			"https://motivational.lehi.dev/2023/04/glory.html",
			"https://motivational.lehi.dev/2023/04/your-time-is-limited.html",
			"https://motivational.lehi.dev/2023/04/for-true-hero-isnt-measured-by-size-of.html",
			"https://motivational.lehi.dev/2015/03/leaders-arent-born-they-are-made.html",
			"https://motivational.lehi.dev/2010/07/saying.html",
			"https://motivational.lehi.dev/2010/07/since-we-cannot-know-all-that-there-is.html",
			"https://motivational.lehi.dev/2010/07/progress.html",
			"https://motivational.lehi.dev/2010/07/favorite.html",
			"https://motivational.lehi.dev/2010/07/never-let-fear-of-striking-out-get-in.html",
			"https://motivational.lehi.dev/2010/07/to-start-off.html",
			"https://tutorials.lehi.dev/",
			"https://tutorials.lehi.dev/2023/04/lab1-wifi-controlled-led-stoplight.html",
			"https://tutorials.lehi.dev/2023/04/systems-engineering-lab2-wifi.html",
			"https://tutorials.lehi.dev/2023/04/systems-engineering-lab-3-machine-to.html",
			"https://tutorials.lehi.dev/2023/04/systems-engineering-lab-4-event-bus.html",
			"https://tutorials.lehi.dev/2023/04/systems-engineering-lab-5-iot-security.html",
			"https://tutorials.lehi.dev/2023/04/systems-engineering-lab-6-iot-user.html",
			"https://tutorials.lehi.dev/2023/04/systems-engineering-project-iot-project.html",
			"https://www.lehi.dev/",
			"https://www.lehi.dev/home",
			"https://www.lehi.dev/about",
			"https://www.lehi.dev/publications"
		] 
	  }
};

request(options, (err, resp, body) => {
console.log(body);
});

