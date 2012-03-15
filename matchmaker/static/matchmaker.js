function Candidate (id) {
	this.id = id;
	this.score = 0;
	this.AddPoints = function(points) {
		return this.score = this.score+points;
	}
}

// Pull unique questions from the cand_info array.
function findUniqueQuestions (cand_info) {
	var allQuestions = new Array();
	for (i=0; i<cand_info.length; i++) {
		allQuestions[i] = cand_info[i].question;
	};
	return jQuery.unique(allQuestions);
}

// Unique questions stored here:
var questions = findUniqueQuestions(cand_info);

function findUniqueCandidates (cand_info) {
	var allCandidates = new Array();
	for (i=0; i<cand_info.length;i++) {
		allCandidates[cand_info[i].candidate] = new Candidate(cand_info[i].candidate);
	};
	return allCandidates;
}

var uCandidates = findUniqueCandidates(cand_info);

console.log(uCandidates[1]);

function getCheckedRadios() {
	var result = $("input:radio:checked").get();
	var columns = $.map(result, function(element) {
		var name = $(element).attr('name');
		var canID = parseInt(name.charAt( name.length-1));
		var score = parseInt($(element).val());
		uCandidates[canID].AddPoints(score);

		return uCandidates[canID].id+" = "+uCandidates[canID].score;
	});
	return columns.join(" | ");
}


$("document").ready(function() {
	$("#mmForm").hide();
	$("#mmStartButton").click(function() {
		$("#mmWelcome").hide();
		$("#mmForm").toggle();
		// Dynamically set up our forms. 
		for (i=questions.length-1; i>=0; i--) {
			$("#mmForm").append(
				"<fieldset class='question_wrapper' id='question_"+i+"'></fieldset>"
			);

			$("#question_"+i).append(
				"<div class='mmQuestion'>"+questions[i]+"</div>"
			);

			for (x=0; x<cand_info.length; x++) {
				if (cand_info[x].question == questions[i]) {
					$("#question_"+i).append(
						"<div class='response_label'>Candidate's response:</div><div class='mmAnswer'>"+cand_info[x].answer+"</div><div class='radio_wrapper'><div id='disagree'>Strongly disagree</div><input type='radio' name='"+i+"_"+cand_info[x].candidate+"' value='-2' /><input type='radio' name='"+i+"_"+cand_info[x].candidate+"' value='-1' /><input type='radio' name='"+i+"_"+cand_info[x].candidate+"' value='0' /><input type='radio' name='"+i+"_"+cand_info[x].candidate+"' value='1' /><input type='radio' name='"+i+"_"+cand_info[x].candidate+"' value='2' /><div id='agree'>Strongly agree</div></div>"
					);
				};
			};
		};

		$("#mmForm").append(
			'<input class="submit_button" id="submit" value="Find me a candidate" type="button">'
		);

		$("#mmForm").formToWizard({ submitButton: 'submit' });


	});

});