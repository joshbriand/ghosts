var ghostToMove = '';
var originalLocation = '';

function init() {
	$('#newGameOption').bind('click', changeUserType);
	$('#continueGameOption').bind('click', changeUserType);
	$('#userOptionsOption').bind('click', changeUserType);
	$('#statsOption').bind('click', changeUserType);
}

var sections = ['#newGame', '#continueGame', '#options', '#statistics'];
var headers = ['#newGameOption', '#continueGameOption', '#userOptionsOption', '#statsOption'];


$('#existing').css('font-weight', 'lighter');
$('#existing').css('border-bottom', 'solid');
$('#existing').css('border-width', '1px');
$('#existing').css('border-bottom-width', '3px');



function changeUserType() {
	if (this.id === 'newGameOption') {
		for (x=0; x<sections.length; x++) {
			$(sections[x]).css('display', 'none');
			$(headers[x]).css('font-weight', 'lighter');
			$(headers[x]).css('border-bottom', 'solid');
			$(headers[x]).css('border-width', '1px');
			$(headers[x]).css('border-bottom-width', '3px');
		}
		$('#newGame').css('display', 'block');
		$(this).css('font-weight', 'bolder');
		$(this).css('border-width', '3px');
		$(this).css('border-bottom', 'none');
	} else if (this.id === 'continueGameOption') {
		for (x=0; x<sections.length; x++) {
			$(sections[x]).css('display', 'none');
			$(headers[x]).css('font-weight', 'lighter');
			$(headers[x]).css('border-bottom', 'solid');
			$(headers[x]).css('border-width', '1px');
			$(headers[x]).css('border-bottom-width', '3px');
		}
		$('#continueGame').css('display', 'block');
		$(this).css('font-weight', 'bolder');
		$(this).css('border-width', '3px');
		$(this).css('border-bottom', 'none');
	} else if (this.id === 'userOptionsOption') {
		for (x=0; x<sections.length; x++) {
			$(sections[x]).css('display', 'none');
			$(headers[x]).css('font-weight', 'lighter');
			$(headers[x]).css('border-bottom', 'solid');
			$(headers[x]).css('border-width', '1px');
			$(headers[x]).css('border-bottom-width', '3px');
		}
		$('#options').css('display', 'block');
		$(this).css('font-weight', 'bolder');
		$(this).css('border-width', '3px');
		$(this).css('border-bottom', 'none');
	} else if (this.id === 'statsOption') {
		for (x=0; x<sections.length; x++) {
			$(sections[x]).css('display', 'none');
			$(headers[x]).css('font-weight', 'lighter');
			$(headers[x]).css('border-bottom', 'solid');
			$(headers[x]).css('border-width', '1px');
			$(headers[x]).css('border-bottom-width', '3px');
		}
		$('#statistics').css('display', 'block');
		$(this).css('font-weight', 'bolder');
		$(this).css('border-width', '3px');
		$(this).css('border-bottom', 'none');
	}
}

init();
