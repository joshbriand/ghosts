$(document).ready(function(){
	var MOVES = {};
	var DEAD = '';
	var ghostToMove = '';
	var originalLocation = '';
	var ORIGINALLOCATION = '';



	function escapeOn(fn) {
		$(document).on('keyup', function(evt) {
			if (evt.keyCode == 27) {
				console.log(esc);
				fn;
			}
		})
	}

	function escapeOff(fn) {
		$(document).off('keyup', function(evt) {
			if (evt.keyCode == 27) {
				console.log(esc);
				fn;
			}
		})
	}

	function submit() {
		console.log('submit');
		var moves = JSON.stringify(MOVES)
		console.log(moves);
		$('#moves').val(moves);
		$('#dead').val(DEAD);
		$('#originalLocation').val(ORIGINALLOCATION);
	}

	function init() {
		console.log('init');
		$('#turnSubmit').css('display', 'none');
		$('#p1b1').off('click');
		$('#p1b2').off('click');
		$('#p1b3').off('click');
		$('#p1b4').off('click');
		$('#p1y1').off('click');
		$('#p1y2').off('click');
		$('#p1y3').off('click');
		$('#p1y4').off('click');
		$('#p2b1').off('click');
		$('#p2b2').off('click');
		$('#p2b3').off('click');
		$('#p2b4').off('click');
		$('#p2y1').off('click');
		$('#p2y2').off('click');
		$('#p2y3').off('click');
		$('#p2y4').off('click');
		$('#p1b1').bind('click', move);
		$('#p1b2').bind('click', move);
		$('#p1b3').bind('click', move);
		$('#p1b4').bind('click', move);
		$('#p1y1').bind('click', move);
		$('#p1y2').bind('click', move);
		$('#p1y3').bind('click', move);
		$('#p1y4').bind('click', move);
		$('#p2b1').bind('click', move);
		$('#p2b2').bind('click', move);
		$('#p2b3').bind('click', move);
		$('#p2b4').bind('click', move);
		$('#p2y1').bind('click', move);
		$('#p2y2').bind('click', move);
		$('#p2y3').bind('click', move);
		$('#p2y4').bind('click', move);
		$('#turnSubmit').bind('click', submit);
	}

	function move() {
		console.log()
		if ($('#turn').html() == 0 || $('#turn').html() == 10 || $('#turn').html() == 20) {
			console.log('starting movement');
			ghostToMove = $(this);
			originalLocation = $(this).parent();
			$(originalLocation).css('background-color', '#0060c1');
			showStartingOptions();
		} else if ($('turn').html() != $('#player').html()) {
			console.log('in progress movement')
			ghostToMove = $(this);
			originalLocation = $(this).parent();
			$(originalLocation).css('background-color', '#0060c1');
			showOptions();
		} else {
			console.log('wait');
		}
	}

	function showStartingOptions () {
		console.log('show starting options');
		var userPlayer = $('#player').html()
		var xRange = [1, 2, 3, 4, 5, 6];
		if (userPlayer == 1) {
			var yRange = [5, 6];
		} else if (userPlayer == 2) {
			var yRange = [1, 2];
		}
		for (x = 0; x < 6; x++) {
			for (y = 0; y < 2; y++) {
				tempLocationString = '#b' + xRange[x] + yRange[y];
				if ($(tempLocationString).children().length == 0) {
					$(tempLocationString).css('background-color', '#00c161');
					$(tempLocationString).bind('click', startingMoveHere);
				}
			}
		}
	}

	function showOptions (clickLocation) {
		console.log('show options');
		var left = '';
		var right = '';
		var forward = '';
		var backward = '';
		var x = Number(originalLocation.attr('id').charAt(1));
		var y = Number(originalLocation.attr('id').charAt(2));
		$('#p1b1').off('click');
		$('#p1b2').off('click');
		$('#p1b3').off('click');
		$('#p1b4').off('click');
		$('#p1y1').off('click');
		$('#p1y2').off('click');
		$('#p1y3').off('click');
		$('#p1y4').off('click');
		$('#p2b1').off('click');
		$('#p2b2').off('click');
		$('#p2b3').off('click');
		$('#p2b4').off('click');
		$('#p2y1').off('click');
		$('#p2y2').off('click');
		$('#p2y3').off('click');
		$('#p2y4').off('click');
		$(ghostToMove).bind('click', moveReset);
		if (x !== 1) {
			tempX = x - 1;
			left = '#b' + tempX + y;
			if ($(left).children().attr('class') !== 'playerGhost') {
				if ($(left).children().attr('id') == 'opponent') {
					$(left).css('background-color', '#c10000');
					$(left).bind('click', attackHere);
				} else {
					$(left).css('background-color', '#00c161');
					$(left).bind('click', moveHere);
				}
			}
		}
		//right
		if (x !== 6) {
			tempX = x + 1;
			right = '#b' + tempX + y;
			if ($(right).children().attr('class') !== 'playerGhost') {
				if ($(right).children().attr('id') == 'opponent') {
					$(right).css('background-color', '#c10000');
					$(right).bind('click', attackHere);
				} else {
					$(right).css('background-color', '#00c161');
					$(right).bind('click', moveHere);
				}
			}
		}
		//forward
		if (y !== 1) {
			tempY = y - 1;
			forward = '#b' + x + tempY;
			if ($(forward).children().attr('class') !== 'playerGhost') {
				if ($(forward).children().attr('id') == 'opponent') {
					$(forward).css('background-color', '#c10000');
					$(forward).bind('click', attackHere);
				} else {
					$(forward).css('background-color', '#00c161');
					$(forward).bind('click', moveHere);
				}
			}
		}
		//backward
		if (y !== 6) {
			tempY = y + 1;
			backward = '#b' + x + tempY;
			if ($(backward).children().attr('class') !== 'playerGhost') {
				if ($(backward).children().attr('id') == 'opponent') {
					$(backward).css('background-color', '#c10000');
					$(backward).bind('click', attackHere);
				} else {
					$(backward).css('background-color', '#00c161');
					$(backward).bind('click', moveHere);
				}
			}
		}
	}

	function startingMoveHere() {
		console.log('starting move here');
		$(originalLocation).css('background-color', '#00c1c1');
		for (gridX = 1; gridX <= 6; gridX++) {
			for (gridY = 1; gridY <= 6; gridY++) {
				if ($('#b' + gridX + gridY).css('background-color') == 'rgb(0, 193, 97)') {
					$('#b' + gridX + gridY).css('background-color','#00c1c1');
					$('#b' + gridX + gridY).off('click');
				}
			}
		}
		$(ghostToMove).off('click');
		$(ghostToMove).bind('click', startingMoveUndo);
		$(this).append(ghostToMove);
		$(this).css('background-color', '#00c1c1');
		MOVES[ghostToMove.attr('id')] = $(this).attr('id')
		$(ghostToMove).children().attr('id', originalLocation.attr('id'));
		ORIGINALLOCATION = originalLocation.attr('id');
		ghostToMove = '';
		originalLocation = '';
		startingTurnComplete();
	}

	function moveHere() {
		console.log('move here');
		for (gridX = 1; gridX <= 6; gridX++) {
			for (gridY = 1; gridY <= 6; gridY++) {
				$('#b' + gridX + gridY).css('background-color','#00c1c1');
			}
		}
		$(this).css('background-color', '#00c161');
		$(this).append(ghostToMove);
		MOVES[ghostToMove.attr('id')] = $(this).attr('id')
		$(ghostToMove).children().attr('id', originalLocation.attr('id'));
		$(ghostToMove).off('click');
		$(ghostToMove).bind('click', moveUndo);
		ORIGINALLOCATION = originalLocation.attr('id');
		ghostToMove = '';
		originalLocation = '';
		$('#turnSubmit').css('display', 'block');
		for (gridX = 1; gridX <= 6; gridX++) {
			for (gridY = 1; gridY <= 6; gridY++) {
				$('#b' + gridX + gridY).off('click');
			}
		}
	}

	function attackHere() {
		console.log('attack here');
		for (gridX = 1; gridX <= 6; gridX++) {
			for (gridY = 1; gridY <= 6; gridY++) {
				$('#b' + gridX + gridY).css('background-color','#00c1c1');
			}
		}
		deadGhost = $(this).children();
		$(this).css('background-color', '#c10000');
		$(this).append(ghostToMove);
		DEAD = deadGhost.parent().attr('id');
		MOVES[ghostToMove.attr('id')] = $(this).attr('id');
		console.log(DEAD);
		tempLocationString = '';
		var stop = 'n';
		for (x=1; x <= 8; x++) {
			tempLocationString = '#s-' + x + '-player';
			if ($(tempLocationString).children().length == 0) {
				if(stop == 'n') {
					$(tempLocationString).append(deadGhost);
					stop = 'y';
				}
			}
		};
		$(ghostToMove).children().attr('id', originalLocation.attr('id'));
		$(ghostToMove).off('click');
		$(ghostToMove).bind('click', attackUndo);
		ORIGINALLOCATION = originalLocation.attr('id');
		ghostToMove = '';
		originalLocation = '';
		$('#turnSubmit').css('display', 'block');

		for (gridX = 1; gridX <= 6; gridX++) {
			for (gridY = 1; gridY <= 6; gridY++) {
				$('#b' + gridX + gridY).off('click');
			}
		}
	}

	function startingMoveUndo() {
		console.log('starting move undo');
		ghostToMove = $(this);
		originalLocation = $(this).children().attr('id');
		delete MOVES[ghostToMove.attr('id')];
		$('#'+originalLocation).append($(this));
		originalLocation = '';
		$(this).children().attr('id', '');
		$(this).off('click');
		$(this).bind('click', move);
		startingTurnComplete();
	}

	function startingTurnComplete () {
		console.log('starting turn complete');
		var complete = 'y';
		tempLocationString = '';
		for (x = 1; x <= 8; x++) {
			tempLocationString = '#s-' + x + '-player';
			console.log($(tempLocationString).children().length);
			if ($(tempLocationString).children().length != 0) {
				complete = 'n';
			}
		}
		if (complete == 'y') {
			$('#turnSubmit').css('display', 'block');
		} else {
			$('#turnSubmit').css('display', 'none');
		}
	}

	function moveReset() {
		console.log('move reset');
		$(ghostToMove).off('click');
		$(ghostToMove).bind('click', move);
		for (gridX = 1; gridX <= 6; gridX++) {
			for (gridY = 1; gridY <= 6; gridY++) {
				$('#b' + gridX + gridY).css('background-color','#00c1c1');
			}
		}
		ghostToMove = '';
		originalLocation = '';
		init();
	}

	function moveUndo() {
		console.log('move undo');
		ghostToMove = $(this);
		$(this).parent().css('background-color','#00c1c1');
		originalLocation = $(this).children().attr('id');
		$(this).children().attr('id', '');
		delete MOVES[ghostToMove.attr('id')];
		$('#'+originalLocation).append($(this));
		originalLocation = '';
		$(this).off('click');
		$(this).bind('click', move);
		init();
	}

	function attackUndo() {
		console.log('attack undo');
		ghostToMove = $(this);
		$(this).parent().css('background-color','#00c1c1');
		originalLocation = $(this).children().attr('id');
		$(this).children().attr('id', '');
		delete MOVES[ghostToMove.attr('id')];
		$('#'+originalLocation).append($(this));
		originalLocation = '';
		$(this).off('click');
		$(this).bind('click', move);
		var deadOriginalLocation = $('#' + DEAD);
		DEAD = '';
		tempLocationString = '';
		var stop = 'n';
		for (x=8; x >= 1; x--) {
			tempLocationString = '#s-' + x + '-player';
			if ($(tempLocationString).children().attr('id') == 'opponent') {
				if(stop == 'n') {
					deadOriginalLocation.append($(tempLocationString).children());
					stop = 'y';
				}
			}
		};
		init()
	}
	//start script
	init();
});
