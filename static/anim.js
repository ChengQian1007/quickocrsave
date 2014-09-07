
var theData = $.ajax({url:"/api/get_all_sources",
                        success:load_data});


function load_data(data) {
    console.log(data);

    j = JSON.parse(data)

var theTemplateScript = $("#header").html();
var theTemplate = Handlebars.compile (theTemplateScript);
var newHTML = theTemplate(data);
$(document.body).append(theTemplate(j));

}

