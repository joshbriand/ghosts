var ghostToMove = '';
var originalLocation = '';

function init() {
	$('#new').bind('click', changeUserType);
	$('#existing').bind('click', changeUserType);
}

function changeUserType() {
	if (this.id === 'new') {
		$('#newUser').css('display', 'block');
		$('#existingUser').css('display', 'none');
		$(this).css('font-weight', 'bolder');
		$('#existing').css('font-weight', 'lighter');
		$(this).css('border-width', '3px');
		$(this).css('border-bottom', 'none');
		$('#existing').css('border-bottom', 'solid');
		$('#existing').css('border-width', '1px');
		$('#existing').css('border-bottom-width', '3px');
	} else if (this.id === 'existing') {
		$('#existingUser').css('display', 'block');
		$('#newUser').css('display', 'none');
		$(this).css('font-weight', 'bolder');
		$('#new').css('font-weight', 'lighter');
		$(this).css('border-width', '3px');
		$(this).css('border-bottom', 'none');
		$('#new').css('border-bottom', 'solid');
		$('#new').css('border-width', '1px');
		$('#new').css('border-bottom-width', '3px');
	}
}

init();
