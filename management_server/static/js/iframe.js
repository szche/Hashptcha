const DICT = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
let currently_working = false;
let solved_data;

// Verification for debugging purposes
// function verify(data) {
// 	fetch('/verify', {
// 		method: 'POST',
// 		headers: {
// 			'Content-Type': 'application/json',
// 		},
// 		body: JSON.stringify(data),
// 	})
// 		.then(response => response.json())
// 		.then(data => {
// 			console.log('Success:', data);
// 		})
// 		.catch((error) => {
// 			console.error('Error:', error);
// 		});
// }

let allStrings = function* (chars) {
	yield '';
	for (let prefix of allStrings(chars)) for (let c of chars) yield `${prefix}${c}`;
};

const hex2bin = (data) => data.split('').map(i =>
	parseInt(i, 16).toString(2).padStart(4, '0')).join('');


async function md5(data) {
	return hashwasm.md5(data);
}

async function sha256(data) {
	return hashwasm.sha256(data);
}

async function start_work(data) {
	currently_working = true;
	let count = 0;
	let data_to_return = {
		"token": data["token"],
		"value": NaN,
	}
	console.log("Difficulty target: ", data["target"].length);
	for (let str of allStrings(DICT)) {
		const value = data['prefix'] + str;
		const value_hashed = await md5(value);
		count++;
		const hash_binary = hex2bin(value_hashed);
		const hash_binary_trimmed = hash_binary.substring(0, data['target'].length);
		if (hash_binary_trimmed == data['target']) {
			data_to_return["value"] = value;
			break;
		}
	}
	console.log("Hashed counter: ", count);
	return data_to_return;
}

function markAsDone() {
	let button = document.getElementById("square-start");
	button.classList.remove('btn-outline-primary');
	button.classList.add('btn-success');
}

function fetchTask() {
	fetch('/get-task')
		.then(response => response.json())
		.then(data => {
			console.log(data);
			const task_completed = start_work(data).then((x) => {
				solved_data = x;
				markAsDone();
				//verify(solved_data); //verification for debuggging purposes
				window.parent.postMessage(solved_data, '*');
				currently_working = false;
			});
		});
}

$("#square-start").click(function () {
	if (currently_working == false) fetchTask();
});