let currently_working = false;
let solved_data;

// Verification for debugging purposes
function verify(data) {
	fetch('/verify', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(data),
	})
		.then(response => response.json())
		.then(data => {
			console.log('Success:', data);
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}

const hex2bin = (data) => data.split('').map(i =>
	parseInt(i, 16).toString(2).padStart(4, '0')).join('');

async function md5(data) {
	return hashwasm.md5(data);
}

async function sha256(data) {
	return hashwasm.sha256(data);
}

async function binary_to_uint8(data) {
	let int8Buffer = [];
	for(let i =0; i<(data.length/8); i++) {
		let chunk = data.substring(i*8, (i+1)*8);
		int8Buffer.push( parseInt(chunk, 2) );
	}
	const uint8Array = new Uint8Array(int8Buffer);
	return uint8Array;
}

async function start_work(data) {
	currently_working = true;
	let data_to_return = {
		"token": data["token"],
		"value": NaN,
	}
	let alg_type = data['hash_type'];
	let hash_func;
	if (alg_type == 'MD5') hash_func = md5;
	else if (alg_type == 'SHA256') hash_func = sha256;
	
	let point = data['start_point'];
	while(true) {
		point = point.padStart(8*Math.ceil(point.length/8), '0');
		let uint8Buffer = await binary_to_uint8(point);
		const value_hashed = await hash_func(uint8Buffer);
		const hash_binary = hex2bin(value_hashed);
		const hash_binary_trimmed = hash_binary.substring(0, data['target'].length);
		if (hash_binary_trimmed == data['target']) {
			data_to_return["value"] = point;
			break;
		}
		point = addBinary(point, '1');
	}
	return data_to_return;
}

function markAsDone() {
	$("#loader").hide();
	$("#task-done").fadeIn();
	$('#task-done').css('display','inline-block');
}

function showLoader() {
	$("#square-start").hide();
	$("#loader").show();
	$('#loader').css('display','inline-block');
}

function fetchTask() {
	showLoader();
	fetch('/get-task')
		.then(response => response.json())
		.then(data => {
			console.log(data);
			const task_completed = start_work(data).then((x) => {
				solved_data = x;
				markAsDone();
				verify(solved_data); //verification for debuggging purposes
				window.parent.postMessage(solved_data, '*');
				currently_working = false;
			});
		});
}

$("#square-start").click(function () {
	if (currently_working == false) fetchTask();
});