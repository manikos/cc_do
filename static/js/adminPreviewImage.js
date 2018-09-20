const $ = django.jQuery;


$(function() {

	$('input[type=file]').each(function() {
		let inputId = this.id;

		$(this).after(`
			<div id="${inputId}-wrapper" style="display:inline-block;">
				<div>
					<strong style="font-size:13px;color:#666;">NEW IMAGE</strong>
					<img id="${inputId}-preview" src="" alt="" style="width:200px;">
				</div>
			</div>
		`);

		$(`#${inputId}-wrapper`).hide();
		$(this).on('change', function() { readFile(this, inputId); });

	});

	function readFile(input, inputId) {
	    if (input.files && input.files[0]) {
	        let reader = new FileReader();
	        reader.onload = function() {
				$(`#${inputId}-preview`).attr('src', reader.result);
				$(`#${inputId}-wrapper`).show();
	        };
	        reader.readAsDataURL(input.files[0]);
	    }
	    else {
	        alert('This browser does not support the FileReader API!');
	    }
	}

});
