$("#compose").click(function(){
    $('#myModal').modal('show')
});

$(document).ready(function() {
    var text_max = 132;
    $('#left_chars').html(text_max + ' characters remaining');
    $('#textarea').keyup(function() {
        var text_length = $('#textarea').val().length;
        var text_remaining = text_max - text_length;
        $('#left_chars').html(text_remaining + ' characters remaining');
    });
});
