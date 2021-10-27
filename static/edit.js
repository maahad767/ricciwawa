//https://www.jqueryscript.net/table/Tiny-jQuery-Plugin-For-Creating-An-Editable-Table-editTable.html
/*
This file is to built editable table to allow a user to modify each word in a story.  Once saved, the story will be updated while the story code remains the same.
*/

function create_table(response){
    cantonses_audio_file = response["filename_trad_mp3"];
    mandarin_audio_file = response["filename_sim_mp3"];
    sim_spaced_sentence = response["text_sim"];
    trad_spaced_sentence = response["text_trad"];
    image_link = response["image_link"];
    pin_yin = response["pin_yin"];
    english_meaning_word = response["english_meaning_word"];
    english_meaning_article = response["english_meaning_article"];
    rows = []
    rows_sim_spaced_sentence = sim_spaced_sentence.split("\n")
    rows_trad_spaced_sentence = trad_spaced_sentence.split("\n") 
    rows_pin_yin = pin_yin.split("\n")
    rows_english_meaning_word = english_meaning_word.split("\n")

    for (var i=0;i<rows_trad_spaced_sentence.length; i++) {
        rows.push({trad:rows_trad_spaced_sentence[i], sim:rows_sim_spaced_sentence[i], pin_yin:rows_pin_yin[i], meaning:rows_english_meaning_word[i] })
    }
    $.each(rows, function(i, item) {
        console.log(item)
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
            $('<td class="editMe">').text(temp_trad),
            $('<td class="editMe">').text(temp_sim),
            $('<td class="editMe">').text(temp_pin_yin),
            $('<td class="editMe">').text(temp_meaning),
            $('<td>').html("<button id='add_" + (i+1) + "'><img src=\"/static/img/plus.svg\">Add</button>&nbsp;&nbsp;<button id='del_" + (i+1) + "'>Del</button>"),
        ).appendTo('#records_table');
    })
    const editor =new SimpleTableCellEditor("records_table");
    editor.SetEditableClass("editMe");

}
function load_json (){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const storycode = urlParams.get('sc')
    console.log(storycode)
    if (storycode != undefined) {
        if (storycode.length>23 && storycode.length<30) {        
            $.ajax({      
                url: '/get_content?&pc='+storycode,
                //data: svg_formdata_ajax,
                type: 'GET',
                success: function (response) { 
                    $('#myModal').modal('hide')
                    console.log(response);
                    create_table(response)
                }
            })
        }
    }

}

$(function() {
    load_json();
})