const hashptcha = new class {
	constructor() {
		this.div = document.querySelector(".hashptcha");
		this.site_key = this.div.getAttribute("site-key");
		this.server_url = "URL_HERE_TBD";
		this.render();
	}

	render() {
		this.iframe = document.createElement("iframe");
		this.iframe.src = this.server_url+'/?'+this.site_key; 
		this.iframe.id="HashptchaIframe";
		this.iframe.width="200px";
		this.iframe.height="60px";
		this.iframe.scrolling="no";
		this.iframe.style.border="0px";
		this.div.appendChild(this.iframe);
	}
}();

