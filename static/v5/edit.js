//https://www.jqueryscript.net/table/Tiny-jQuery-Plugin-For-Creating-An-Editable-Table-editTable.html
/*
This file is to built editable table to allow a user to modify each word in a story.  Once saved, the story will be updated while the story code remains the same.
*/


//===================================================================
// Copy element to clipboard
//===================================================================
function public_code_copy(elementId){
    // Create a "hidden" input
    var aux = document.createElement("input");

    // Assign it the value of the specified element
    aux.setAttribute("value", document.getElementById(elementId).innerHTML);

    // Append it to the body
    document.body.appendChild(aux);

    // Highlight its content
    aux.select();

    // Copy the highlighted text
    document.execCommand("copy");

    // Remove it from the body
    document.body.removeChild(aux);
}

//get contents from all rows to current__rows
function collect_table_contents(){
    current_rows = []
    var table = document.getElementById("records_table");
    for (var i = 1, row; row = table.rows[i]; i++) {
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       current_rows.push({trad:row.cells[1].textContent, sim:row.cells[2].textContent, pin_yin:row.cells[3].textContent, meaning:row.cells[4].textContent})
    }
    console.log(current_rows)
    return current_rows;
}

//function add_row()
//response is the json data
//row_id is to insert/delete new row
//action - add or delete, copy from the row below, duplicate
function create_table(rows){   
    $('#records_table').html("<tr><th></th><th>Traditional</th><th>Simplified</th><th>Pin yin</th><th>Meaning</th>    <th>Add/Delete<BR>Copy/Repeat</th></tr>")
    $.each(rows, function(i, item) {
        temp_trad = item.trad;
        temp_sim = item.sim;
        temp_pin_yin = item.pin_yin;
        temp_meaning = item.meaning;
        if (temp_sim == "BBHHHAAAA70707BBHHHAAAA70707"){
            temp_sim = "[New Line 新段落]";
            temp_trad = "[New Line 新段落]";
            temp_pin_yin = "[New Line 新段落]";
            temp_meaning = "[New Line 新段落]";
        }
        var $tr = $('<tr>').append(
            $('<td>').text(i+1),
            $('<td id="trad_' + (i+1)  + '" class="edit_trad_td">').text(temp_trad),
            $('<td id="sim_' + (i+1)  + '"class="edit_sim_td">').text(temp_sim),
            $('<td id="pin_yin_' + (i+1)  + '"class="edit_pin_yin_td">').text(temp_pin_yin),
            $('<td id="meaning_' + (i+1)  + '"class="edit_meaning_td">').text(temp_meaning),
            $('<td>').html("<button class=\"button_add\" id='add_" + (i+1) + "'><img style=\"margin-bottom:3px;\" width='15px' src=\"/static/img/plus-circle.svg\"></button>&nbsp;<button class=\"button_del\"  id='del_" + (i+1) + "'><img style=\"margin-bottom:3px;\" width='15px' src=\"/static/img/minus-circle.svg\"></button>&nbsp;<button class=\"button_copy\" id='copy_" + (i+1) + "'>C</button>&nbsp;<button class=\"button_repeat\" id='dup_" + (i+1) + "'>R</button>"),
        ).appendTo('#records_table');    
    })
    $(".button_add").click(function(){
        console.log(this);
        
        row_number = (this.id).substring(4);
        collected_rows = collect_table_contents()        
        //var row = document.getElementById("records_table").insertRow(row_number);
        new_rows = []
        $.each(collected_rows, function(i, item) {
            if (i==row_number){
                new_rows.push({trad:"", sim:"", pin_yin:"", meaning:""})
            }
            new_rows.push({trad:collected_rows[i].trad, sim:collected_rows[i].sim, pin_yin:collected_rows[i].pin_yin, meaning:collected_rows[i].meaning})
        })
        create_table(new_rows);       
    });
    $(".button_del").click(function(){
        console.log(this);       
        //need to minus 1 because id starts from 1 while loop starts from 0
        row_number = parseInt((this.id).substring(4))-1;
        collected_rows = collect_table_contents()        
        //var row = document.getElementById("records_table").insertRow(row_number);
        new_rows = []
        $.each(collected_rows, function(i, item) {
            if (i!=row_number){
                new_rows.push({trad:collected_rows[i].trad, sim:collected_rows[i].sim, pin_yin:collected_rows[i].pin_yin, meaning:collected_rows[i].meaning})
            }
        })
        create_table(new_rows);       
    });
    //copy from below
    $(".button_copy").click(function(){
        console.log(this);       
        //need to minus 1 because id starts from 1 while loop starts from 0
        row_number = parseInt((this.id).substring(5))-1;
        collected_rows = collect_table_contents()  
        //var row = document.getElementById("records_table").insertRow(row_number);
        new_rows = []
        $.each(collected_rows, function(i, item) {
            //copy from below
            if (i==row_number){
                //make sure the next row exist
                if (collected_rows[i+1] != undefined) {
                    collected_rows[i].trad = collected_rows[i].trad + collected_rows[i+1].trad;
                    collected_rows[i].sim = collected_rows[i].sim + collected_rows[i+1].sim;
                    collected_rows[i].pin_yin = collected_rows[i].pin_yin + " " + collected_rows[i+1].pin_yin;
                    collected_rows[i].pin_yin = collected_rows[i].pin_yin.replace(/ +/g, ' ').trim();
                    collected_rows[i].meaning = collected_rows[i].meaning + " " + collected_rows[i+1].meaning;
                }
                //regardless if the next row exist or not, update new rows
            }
            new_rows.push({trad:collected_rows[i].trad, sim:collected_rows[i].sim, pin_yin:collected_rows[i].pin_yin, meaning:collected_rows[i].meaning})
        })
        create_table(new_rows);       
    });    
    $(".button_repeat").click(function(){
        console.log(this);
        //need to minus 1 because id starts from 1 while loop starts from 0
        row_number = parseInt((this.id).substring(4))-1;
        collected_rows = collect_table_contents()        
        //var row = document.getElementById("records_table").insertRow(row_number);
        new_rows = []
        $.each(collected_rows, function(i, item) {
            if (i==row_number){
                new_rows.push({trad:collected_rows[i].trad, sim:collected_rows[i].sim, pin_yin:collected_rows[i].pin_yin, meaning:collected_rows[i].meaning})
            }
            new_rows.push({trad:collected_rows[i].trad, sim:collected_rows[i].sim, pin_yin:collected_rows[i].pin_yin, meaning:collected_rows[i].meaning})
        })
        create_table(new_rows);       
    });    
}
var lang="";
var image_link="";

function load_json (){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const storycode = urlParams.get('sc')
    console.log(storycode)
    if (storycode != undefined) {
        if (storycode.length>23 && storycode.length<30) {        
            $.ajax({      
                url: '/get_content?mp3=No&pc='+storycode,
                //data: svg_formdata_ajax,
                type: 'GET',
                success: function (response) { 
                    $('#myModal').modal('hide')
                    console.log(response);
                    cantonses_audio_file = response["filename_trad_mp3"];
                    mandarin_audio_file = response["filename_sim_mp3"];
                    sim_spaced_sentence = response["text_sim"];
                    trad_spaced_sentence = response["text_trad"];
                  
                    $("#story_title").val(response["story_title"]);
                    $("#story_author").val(response["story_author"]);
                    $("#story_source").val(response["story_source"]);
                    $("#story_tags").val(response["story_tags"]);
                    $("#story_category").val(response["story_category"]);
                    $("#story_difficulty").val(response["story_difficulty"]);

                    image_link = response["image_link"];
                    pin_yin = response["pin_yin"];
                    english_meaning_word = response["english_meaning_word"];
                    english_meaning_article = response["english_meaning_article"];
                    lang = response["lang"]
                    rows = []
                    rows_sim_spaced_sentence = sim_spaced_sentence.split("\n")
                    rows_trad_spaced_sentence = trad_spaced_sentence.split("\n") 
                    rows_pin_yin = pin_yin.split("\n")
                    rows_english_meaning_word = english_meaning_word.split("\n")
                    for (var i=0;i<rows_trad_spaced_sentence.length; i++) {
                        rows.push({trad:rows_trad_spaced_sentence[i], sim:rows_sim_spaced_sentence[i], pin_yin:rows_pin_yin[i], meaning:rows_english_meaning_word[i] })
                    }
                    create_table(rows)

                    if (image_link!="undefined")
                        $("#image_link").val(image_link);
                    if (english_meaning_article!="undefined")
                        $("#translated_text").val(english_meaning_article);    
                    $('#myModal').modal('hide')    

                }
            })
        }
    }
}

//get data from the table and then send to the server
function save_edit (){
    $('#myModal').modal('show')

    var trad=[];
    var sim=[];
    var pin_yin=[];
    var meaning=[];
    $("#records_table tr").each(function () {
        //loop through each row
        $('td', this).each(function () {
            var value = $(this).text();
            var id = $(this).attr('id')
            console.log(id)
            if (id != undefined) {
                if (id.includes("trad")) {
                    trad.push(value)
                }
                else if (id.includes("sim")) {
                    sim.push(value)
                }
                else if (id.includes("pin_yin")) {
                    pin_yin.push(value)
                }
                else if (id.includes("meaning")) {
                    meaning.push(value)
                }           
            }
        })    
    })
    story_title = $("#story_title").val()
    story_author = $("#story_author").val()
    story_source = $("#story_source").val()
    story_tags = $("#story_tags").val()
    story_difficulty = $("#story_difficulty").val()
    story_category = $("#story_category").val()


    //check if use the same story code
    var keep_sc = 0;
    if ($("#keep_sc")[0].checked == true)
        keep_sc=1;
    var image_link = $("#image_link").val();
    var translated_text = $("#translated_text").val().replace(/\r/g,"<BR>").replace(/\n/g,"<BR>");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    formdata = {"trad":trad, "sim":sim, "pin_yin":pin_yin, "meaning":meaning, "sc":urlParams.get('sc'), "keep_sc":keep_sc, "lang":lang, "image_link":image_link, "english_meaning_article":translated_text, "story_title":story_title, "story_author":story_author, "story_source":story_source, "story_tags":story_tags, "story_category":story_category, "story_difficulty":story_difficulty}
    //https://mkyong.com/jquery/jquery-ajax-submit-a-multipart-form/
    $.ajax({      
        url: '/save_edit',
        data: JSON.stringify(formdata),
        type: 'POST',
        dataType: 'json',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, // NEEDED, DON'T OMIT THIS
        success: function (response) { 
            console.log(response);
            //var obj = JSON.parse(response);
            $("#span_public_article_code").html('https://www.ricciwawa.com/?sc='+response["public_code"]);
            $("#div_public_article_code").show();
            $('#myModal').modal('hide')
        }
    })
}


$(function() {
    $('#myModal').modal('show')
    load_json();    
    const editor =new SimpleTableCellEditor("records_table");
    editor.SetEditableClass("edit_trad_td");
    editor.SetEditableClass("edit_sim_td");
    editor.SetEditableClass("edit_pin_yin_td");
    editor.SetEditableClass("edit_meaning_td");
    $('#save_edit').click(function() {save_edit();});
})