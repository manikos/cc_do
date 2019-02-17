$(function() {

	$('.inline-related:not(.empty-form) input[type=file]').each(function() {
		addExtraInfo(this);
	});

	$(".add-row").on("click", function() {
		let imageDiv = $(this).prevAll(".inline-related.last-related:not(.empty-form)").first();
		let imageInput = imageDiv.find("input[type=file]");
		addExtraInfo(imageInput);
	});

	function addExtraInfo(el) {
		let jEl = $(el);
		let inputId = jEl.attr("id");
		jEl.after(`
			<div id="${inputId}-wrapper" style="display:inline-block;">
				<div style="display:flex;flex-flow:column;align-items:center;">
					<strong style="font-size:13px;color:#666;">NEW IMAGE</strong>
					<img id="${inputId}-preview" src="" alt="" style="width:200px;">
					<strong id="${inputId}-info" style="margin:0;"></strong>
				</div>
			</div>
		`);
		$(`#${inputId}-wrapper`).hide();
		jEl.on('change', function() { readFile(this, inputId); });
	}

	function readFile(input, inputId) {
	    if (input.files && input.files[0]) {
	    	let info = $(`#${inputId}-info`);
	        let reader = new FileReader();
	        reader.onload = function(f) {
	        	let image = new Image();
	        	image.src = f.target.result;
	        	image.onload = function() {
			        $(`#${inputId}-preview`).attr('src', reader.result);
					$(`#${inputId}-wrapper`).show();
			        info.empty().append(`<span>${this.width} x ${this.height}px</span>`);
		        };
	        };
	        reader.readAsDataURL(input.files[0]);
	    }
	    else {
	        alert('This browser does not support the FileReader API!');
	    }
	}

});
