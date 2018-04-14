$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }
function submitForm(val){
    var frm = $('#v_form');
	frm.submit(function (ev) {
			ev.preventDefault();
			$.ajax({
			//console.log("Motherfucker");
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize() + "&data=" + val,		
            success: function (data) {
			$('#v_form').unbind('submit').submit;
            }
        });
});
}



