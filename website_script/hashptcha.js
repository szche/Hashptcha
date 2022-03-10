const hashptcha = new class {
	constructor() {
		this.div = document.querySelector(".hashptcha");
		this.site_key = this.div.getAttribute("site-key");
		this.server_url = "http://127.0.0.1:5000/frame";
		this.render();
		this.listen();
	}

	render() {
		this.iframe = document.createElement("iframe");
		this.iframe.src = this.server_url + '?' + this.site_key;
		this.iframe.id = "HashptchaIframe";
		this.iframe.width = "250px";
		this.iframe.height = "60px";
		this.iframe.scrolling = "no";
		this.iframe.style.border = "0px";
		this.iframe.style.marginTop = "20px";
		this.iframe.style.marginBottom = "20px";
		this.div.appendChild(this.iframe);
	}

	listen() {
		window.addEventListener('message', function (e) {
			const data = e.data;
			const data_string = JSON.stringify(data)
			console.log("Got a new message", data);
			if ($('#hashptcha-answer').length > 0) {
				$('#hashptcha-answer').val(data_string);
			}
			else {
				this.input = this.document.createElement("input");
				this.input.type = "hidden";
				this.input.id = "hashptcha-answer";
				this.input.value = data_string;
				document.querySelector(".hashptcha").appendChild(this.input);
			}
		});
	}

}();
