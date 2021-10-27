var inputtext_temp_hold=""
var audio_playing_counter = 0;
var audio_svg = document.getElementById("audio_svg");
var pause_audio_time=0;
var load_text = [];
//testing code
//Z3BkeWMxMjAzMjMxNTQ2aXZjbG0=
temp_base64=[];
map_character_sentence=[];


function change_language(value) {
   var parser = document.createElement('a');
   var url = [location.protocol, '//', location.host, location.pathname].join('');
   parser.href = url;
   parser.search = '?lang=' + value;
   window.location.href = parser.href
}
  

//============================================================
//perform display when a button is clicked
function button_click(item) {
    if (item == "hide radical") {
        $('.class_sim_png').hide();
        $('.class_trad_png').hide();         
        if ($("#t_or_s_t")[0].checked == true)
        {
            $('.class_trad_text').show();
            $('.class_sim_text').hide();            
        }
        if ($("#t_or_s_s")[0].checked == true)
        {
            $('.class_trad_text').hide();
            $('.class_sim_text').show();
        }
    }
    if (item == "show radical") {
        $('.class_sim_text').hide();            
        $('.class_trad_text').hide();
        if ($("#t_or_s_t")[0].checked == true)
        {
            $('.class_trad_png').show();
            $('.class_sim_png').hide();            
        }
        if ($("#t_or_s_s")[0].checked == true)
        {
            $('.class_sim_png').show();
            $('.class_trad_png').hide();
        }
    }
    //hide image that cannot be shown
    //run this after images are displayed
    document.querySelectorAll('img').forEach(function(img){
        img.onerror = function(){
            this.style.display='none';
        };
    })

}


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

//===================================================================
// Get the code from the user, retrieve the content, and display them
// cHF0eGUxMjAyMTYyNTM1aGF4cmY
//===================================================================
function code_entered(){
    in_code_entered = $("#input_article_code").val();
    console.log(in_code_entered);
    $('#myModal').modal('show')
    //merge with convert code
    if (in_code_entered.length>23 && in_code_entered.length<30) {        
        $.ajax({      
            url: '/get_content?mp3=y&pc='+in_code_entered,
            //data: svg_formdata_ajax,
            type: 'GET',
            success: function (response) { 
               $('#myModal').modal('hide')
                console.log(response);
                $("#inputtext").val(response["input_text"])
                cantonses_audio_file = response["filename_trad_mp3"];
                mandarin_audio_file = response["filename_sim_mp3"];
                sim_spaced_sentence = response["text_sim"];
                trad_spaced_sentence = response["text_trad"];
                image_link = response["image_link"];
                pin_yin = response["pin_yin"];
                english_meaning_word = response["english_meaning_word"];
                english_meaning_article = response["english_meaning_article"];
                show_analyzed_text(sim_spaced_sentence, trad_spaced_sentence, pin_yin, english_meaning_word, english_meaning_article);
                if (image_link != "") {
                    $("#public_article_img").attr("src",image_link);
                    $("#div_public_article_img").show();
                }
                //check if the audio file is ready
                if (cantonses_audio_file != undefined) {                    
                    $("#trad_audio_text").attr("src","data:audio/mp3;base64," + cantonses_audio_file);
                    //set the session storage to done if files are downloaded successfully
                    sessionStorage.setItem("cantonese_audio_download", "done");
                    $("#div_audio").show()
                }
                //check if the audio file is ready
                if (mandarin_audio_file != undefined) {
                    $("#sim_audio_text").attr("src","data:audio/mp3;base64," + mandarin_audio_file);
                    //set the session storage to done if files are downloaded successfully
                    sessionStorage.setItem("mandarin_audio_download", "done");
                    $("#div_audio").show()
                }
                $("#text_analysis").show(); 
            }
        })
    }
}


//============================================================
//write to div processed_text_analysis_text - TW or HK
function show_analyzed_text_trans(in_eng_spaced_sentence, in_trans_meaning_word, in_trans_meaning_article){
    span_text =""
     $("#processed_text_analysis_text").html("")
     each_word_array = []
     pevious_word = ""
     eng_spaced_sentence = in_eng_spaced_sentence.split("\n")
     trans_meaning_word = in_trans_meaning_word.split("\n")
     word_meaning_html =""
     //to check if the text has a emoji
     $('#translated_text').html(in_trans_meaning_article.replace(/BBHHHAAAA70707/g,"<BR>"))
 
      //loop through the setence
     for (var counter=0; counter< eng_spaced_sentence.length; counter++){
 
         each_word_eng=eng_spaced_sentence[counter]
         each_trans_meaning_word=trans_meaning_word[counter]

         //loop through each word
         ascii_indicator = true
         //if not line break
         if (!each_word_eng.includes("BBHHHAAAA70707") && !each_word_eng.includes("<BR>")) {
             //loop through the word to find the URL of each character in the word
             span_text = span_text + "<span class='span_char' style='white-space: nowrap;width:auto;padding-right:1em;'><p class='class_normal_text'>" + each_word_eng + "</p>" + "<p class='class_meaning span_p_char'>" + each_trans_meaning_word + "</p></span>";
         }
         else
             span_text = span_text + "<BR><BR>"           
     }
     $("#processed_text_analysis_text").html(span_text)
     button_click("hide radical");
     $("#pin_yin_on_off").click(function(){
         if (this.checked == true) 
             $('.class_pin_yin').show();
         else
             $('.class_pin_yin').hide();
     })
     $("#meaning_on_off").click(function(){
         if (this.checked == true) 
             $('.class_meaning').show();
         else
             $('.class_meaning').hide();        
     })
     $("#radical_on_off").on("click", function() {
         if (this.checked == true)
         {
             //hide text and show radical
             $('.class_trad_text').hide();
             $('.class_sim_text').hide();
             button_click("show radical");
         }
         else
         {
             //show text and hide radical
             $('.class_sim_png').hide();
             $('.class_trad_png').hide();            
             button_click("hide radical");
         }
     })
     //traditional button clicked
     $("#t_or_s_t").on("click", function() {
         if ($("#radical_on_off")[0].checked == true)
             button_click("show radical");
         else
             button_click("hide radical");
     })
     //simplified button clicked
     $("#t_or_s_s").on("click", function() {
         if ($("#radical_on_off")[0].checked == true)
             button_click("show radical");
         else
             button_click("hide radical");
     })    
 
 }

 

//============================================================
//write to div processed_text_analysis_text - TW or HK
function show_analyzed_text(in_sim_spaced_sentence, in_trad_spaced_sentence, in_pin_yin, in_english_meaning_word, english_meaning_article){
   span_text =""
    $("#processed_text_analysis_text").html("")
    each_word_array = []
    pevious_word = ""
    pin_yin = in_pin_yin.split("\n")
    sim_spaced_sentence = in_sim_spaced_sentence.split("\n")
    trad_spaced_sentence = in_trad_spaced_sentence.split("\n")
    english_meaning_word = in_english_meaning_word.split("\n")
    word_meaning_html =""
    //to check if the text has a emoji
    const regex = /(?:[\u2700-\u27bf]|(?:\ud83c[\udde6-\uddff]){2}|[\ud800-\udbff][\udc00-\udfff]|[\u0023-\u0039]\ufe0f?\u20e3|\u3299|\u3297|\u303d|\u3030|\u24c2|\ud83c[\udd70-\udd71]|\ud83c[\udd7e-\udd7f]|\ud83c\udd8e|\ud83c[\udd91-\udd9a]|\ud83c[\udde6-\uddff]|\ud83c[\ude01-\ude02]|\ud83c\ude1a|\ud83c\ude2f|\ud83c[\ude32-\ude3a]|\ud83c[\ude50-\ude51]|\u203c|\u2049|[\u25aa-\u25ab]|\u25b6|\u25c0|[\u25fb-\u25fe]|\u00a9|\u00ae|\u2122|\u2139|\ud83c\udc04|[\u2600-\u26FF]|\u2b05|\u2b06|\u2b07|\u2b1b|\u2b1c|\u2b50|\u2b55|\u231a|\u231b|\u2328|\u23cf|[\u23e9-\u23f3]|[\u23f8-\u23fa]|\ud83c\udccf|\u2934|\u2935|[\u2190-\u21ff])/g;
    $('#translated_text').html(english_meaning_article.replace(/BBHHHAAAA70707/g,"<BR>"))

     //loop through the setence
    for (var counter=0; counter< trad_spaced_sentence.length; counter++){

        each_word_sim=sim_spaced_sentence[counter]
        each_word_trad=trad_spaced_sentence[counter]
        each_word_pin_yin=pin_yin[counter]
        each_english_meaning_word=english_meaning_word[counter]
        //loop through each word
        a_png_sim_url = []
        a_png_trad_url = []

        png_sim_url=""
        png_trad_url=""
        // if contain at least one Chinese character, this will become False
        // use for adjusting spacing
        ascii_indicator = true
        //if not line break
        if (!each_word_trad.includes("BBHHHAAAA70707") && !each_word_trad.includes("<BR>")) {
            //loop through the word to find the URL of each character in the word
            for (var png_counter=0; png_counter<each_word_trad.length; png_counter++){
                //puncutation
                if (each_word_trad[png_counter] == "，")
                {
                    png_sim_url=png_sim_url+"<p class='class_sim_png'>，</p>";
                    png_trad_url=png_trad_url+"<p class='class_trad_png'>，</p>";   
                }
                else if (each_word_trad[png_counter] == "。")
                {
                    png_sim_url=png_sim_url+"<p class='class_sim_png'>。</p>";   
                    png_trad_url = png_trad_url  +"<p class='class_trad_png'>。</p>";   
                }
                else if (each_word_trad[png_counter] != "")
                {     
                    emoji_flag = false;

                    try {
                        sim_unicode = encodeURIComponent(each_word_sim[png_counter]).replace(/\%/g,"x").toLowerCase()
                    }
                    catch {
                        //check if the character also has problen
                        if (png_counter<each_word_sim.length) {
                            try {
                                test=encodeURIComponent(each_word_sim[png_counter]).replace(/\%/g,"x").toLowerCase()
                            }
                            //error or emoji
                            catch {
                                sim_word = each_word_sim[png_counter] + each_word_sim[png_counter+1];
                                emoji_flag = true
                                //emoji is double chart, so do not loop
                            }
                        }
                    }
                    try {
                        trad_unicode = encodeURIComponent(each_word_trad[png_counter]).replace(/\%/g,"x").toLowerCase()
                    }
                    catch {
                        //check if the character also has problen
                        if (png_counter<each_word_trad.length) {
                            try {
                                test=encodeURIComponent(each_word_trad[png_counter]).replace(/\%/g,"x").toLowerCase()
                            }
                            //error or emoji
                            catch {
                                trad_word = each_word_trad[png_counter] + each_word_trad[png_counter+1];
                                emoji_flag = true
                                //emoji is double chart, so do not loop
                            }
                        }
                    }
                    //don't get the image for English and puncutation                    
                    if (sim_unicode.length > 4 && !emoji_flag){ //print non-English and non-number
                        //png_sim_url=png_sim_url+"<img class='class_sim_png' src='/get_char?char_id="+sim_unicode.toLowerCase()+"_radical_50.png' alt='" +  each_word_sim[png_counter] + "'>"
                        //png_trad_url=png_trad_url+"<img class='class_trad_png' src='/get_char?char_id="+trad_unicode+"_radical_50.png' alt='" +  each_word_trad[png_counter] + "'>"
                        png_sim_url=png_sim_url+"<img class='class_sim_png' width=50px src='/get_char?char_id="+sim_unicode.toLowerCase()+".svg' alt='" +  each_word_sim[png_counter] + "'/>"
                        png_trad_url=png_trad_url+"<img class='class_trad_png' width=50px src='/get_char?char_id="+trad_unicode+".svg' alt='" +  each_word_trad[png_counter] + "'>"                        
                        ascii_indicator = false
                    }
                    else {
                        if (emoji_flag) {
                            png_sim_url = png_sim_url + "<span class='class_sim_png'>" + sim_word + "</span>"
                            png_trad_url = png_trad_url + "<span class='class_trad_png'>" + trad_word + "</span>"

                        }
                        else {
                            png_sim_url = png_sim_url + "<span class='class_sim_png'>" + each_word_sim[png_counter] + "</span>"
                            png_trad_url = png_trad_url + "<span class='class_trad_png'>" + each_word_trad[png_counter] + "</span>"
                        }
                    }
                    if (emoji_flag == true)
                        png_counter = png_counter + 1;
                }
            }
            if (!ascii_indicator) {
                //Chinese word
                span_text = span_text + "<span class='span_char' style='white-space: nowrap;width:auto;padding-right:1em;'>" + "<p class='class_pin_yin span_p_char'>" + each_word_pin_yin + "</p>" +png_sim_url + png_trad_url + "<p class='class_normal_text class_sim_text'>" + each_word_sim + "</p>" + "<p class='class_normal_text class_trad_text'>" + each_word_trad + "</p>" + "<p class='class_meaning span_p_char'>" + each_english_meaning_word + "</p></span>";
            }
            else {
                //non Chinese word
                span_text = span_text + "<span class='span_char' style='white-space: nowrap;width:auto;'>" + "<p class='class_pin_yin span_p_char'>&nbsp;</p>" +png_sim_url + png_trad_url + "<p class='class_normal_text class_sim_text'>" + each_word_sim + "</p>" + "<p class='class_normal_text class_trad_text'>&nbsp;&nbsp;" + each_word_trad + "&nbsp;&nbsp;</p>" + "<p class='class_meaning span_p_char'> </p></span>";
            }
            //console.log(each_word_trad, each_word_sim, each_word_pin_yin, each_english_meaning_word)
        }
        else
            span_text = span_text + "<BR><BR>"           
    }
    $("#processed_text_analysis_text").html(span_text)
    button_click("hide radical");
    $("#pin_yin_on_off").click(function(){
        if (this.checked == true) 
            $('.class_pin_yin').show();
        else
            $('.class_pin_yin').hide();
    })
    $("#meaning_on_off").click(function(){
        if (this.checked == true) 
            $('.class_meaning').show();
        else
            $('.class_meaning').hide();        
    })
    $("#radical_on_off").on("click", function() {
        if (this.checked == true)
        {
            //hide text and show radical
            $('.class_trad_text').hide();
            $('.class_sim_text').hide();
            button_click("show radical");
        }
        else
        {
            //show text and hide radical
            $('.class_sim_png').hide();
            $('.class_trad_png').hide();            
            button_click("hide radical");
        }
    })
    //traditional button clicked
    $("#t_or_s_t").on("click", function() {
        if ($("#radical_on_off")[0].checked == true)
            button_click("show radical");
        else
            button_click("hide radical");
    })
    //simplified button clicked
    $("#t_or_s_s").on("click", function() {
        if ($("#radical_on_off")[0].checked == true)
            button_click("show radical");
        else
            button_click("hide radical");
    })    

}

function TransferCompleteCallback(content){
    // we might want to use the transferred content directly
    // for example to render an uploaded image
}
//============================================
function _(el) {
  return document.getElementById(el);
}      


function uploadFile() {
   var file = _("input_image_file").files[0];
   var file_name = file.name; 
   var form = $("#OCRphotoform")
   console.log(form[0])
   var formdata = new FormData(form[0]);
   $("#loading_spinner").show()
   $("#btn_submit").prop('disabled', true);
   console.log(formdata);
   $('#myModal').modal('show')
   time_dalay = [7,10,12,14,17,22,30,35,45,50,55]
   $.ajax({
         url: '/ocr_process',
         data: formdata,
         type: 'POST',
         contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
         processData: false, // NEEDED, DON'T OMIT THIS
         // ... Other options like success and etc
         success: function (response) { 
            console.log(response);
            obj = response;
            id = obj["id"];

            ocr_sentence = "";
            cantonses_audio_file = id+"_trad.mp3";
            mandarin_audio_file = id+"_sim.mp3";
            sim_text = "";
            trad_text = "";
            sim_spaced_sentence = ""
            trad_spaced_sentence = ""
            //loop to check if the audio files are avaliable
            //set the audio_download flag to false to indicates audio files are not downloaded
            sessionStorage.setItem("cantonese_audio_download", "false");
            sessionStorage.setItem("mandarin_audio_download", "false");
            sessionStorage.setItem("ocr_image_download", "false");
            for (var i = 0; i < 10; i++) {
               setTimeout(function(){
                  if (sessionStorage.getItem("ocr_image_download") != "done") {
                     $.ajax({
                        url: '/check_file?file_name='+id+"_ocr.jpg",
                        type: 'GET',
                        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                        processData: false, // NEEDED, DON'T OMIT THIS
                        // ... Other options like success and etc
                        success: function (response_check_file) { 
                           //check if response has yes, if so the file exists
                           if (response_check_file == "yes\n") {
                              $("#img_ocr_image").attr("src","/get_image?img_id="+id+"_ocr.jpg");
                              //set the session storage to done if files are downloaded successfully
                              sessionStorage.setItem("ocr_image_download", "done");
                              $('#nav_link_4').click() //goto to enter text
                              $('#myModal').modal('hide')
                           }
                        }
                     })
                  }
               }, time_dalay[i]*1000)
            }
            for (var i = 0; i < 10; i++) {
               setTimeout(function(){
                  if (sessionStorage.getItem("cantonese_audio_download") != "done") {
                     $.ajax({
                        url: '/check_file?file_name='+cantonses_audio_file,
                        type: 'GET',
                        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                        processData: false, // NEEDED, DON'T OMIT THIS
                        // ... Other options like success and etc
                        success: function (response_check_file) { 
                           //check if response has yes, if so the file exists
                           if (response_check_file == "yes\n") {
                              $("#trad_audio").attr("src","/get_audio?audio_id="+cantonses_audio_file);
                              //set the session storage to done if files are downloaded successfully
                              sessionStorage.setItem("cantonese_audio_download", "done");
                           }
                        }
                     })
                  }
                  if (sessionStorage.getItem("mandarin_audio_download") != "done") {
                     $.ajax({
                        url: '/check_file?file_name='+mandarin_audio_file,
                        type: 'GET',
                        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                        processData: false, // NEEDED, DON'T OMIT THIS
                        // ... Other options like success and etc
                        success: function (response_check_file) { 
                           //check if response has yes, if so the file exists
                           if (response_check_file == "yes\n") {
                              $("#sim_audio").attr("src","/get_audio?audio_id="+mandarin_audio_file);
                              //set the session storage to done if files are downloaded successfully
                              sessionStorage.setItem("mandarin_audio_download", "done");
                           }
                        }
                     })
                  }
               }, time_dalay[i]*1000)
            }           
         },
         error: function(){
            alert('Error of processing the image.');
            $('#myModal').modal('hide')
         }
   });;       

}

function call_tts_ajax (i,formdata,sentences) {
   console.log(i,sentences[i])
   formdata.index=i;
   formdata.inputtext=sentences[i];
   formdata_ajax = new FormData();
   formdata_ajax.append("text",sentences[i]);
   formdata_ajax.append("index",i);
   formdata_ajax.append("lang",$("#lang").val());
   $("#div_audio").show()
   $.ajax({
         //url: '/makeaudio',
         url: 'getsavedtext',
         data: formdata_ajax,
         type: 'GET',
         contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
         processData: false, // NEEDED, DON'T OMIT THIS
         // ... Other options like success and etc
         success: function (response) {            
            var obj = JSON.parse(response);
            temp_base64[obj.index]=obj.voicedata;   
            //add five seconds to delay hiding of modal
            setTimeout(function(){
               $(".audio_buttons").show();
               $('#myModal').modal('hide');
            },5000);
            //if (i+1 < sentences.length) {
            //   i++;
            //   call_tts_ajax (i,formdata,sentences);               
            //}
         },
         timeout: 120000
   })   
}


//call English TTS server

function create_svg_audio_eng() {
    var form = $("#create_svg_audio_eng")

    //text and image
    var formdata = new FormData(form[0]);
    var svg_formdata = {"inputtext":$("#inputtext").val(),"lang":$("#lang").val(),"index":0};
    var sentences = ($("#inputtext").val()).split(/(?=[。，.,]+)/);
    //$("#create_svg_audio_submit").prop('disabled', true);
    $('#myModal').modal('show')
    svg_formdata_ajax= new FormData();
    svg_formdata_ajax.append("text",$("#inputtext").val());
    time_dalay = [15,22,30,35,45,50,55]
    $("#translated_text").html("");
    $("#span_public_article_code").html("");
    $("#processed_text_analysis_text").html("");
    sessionStorage.setItem("trans_audio_download", "")
    sessionStorage.setItem("text_analysis", "");
    $("#div_audio").hide()

    //list which characters belong to a sentence 
    $.ajax({      
        url: '/converteng',
        //data: svg_formdata_ajax,
        data: formdata,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, // NEEDED, DON'T OMIT THIS
        success: function (response) { 
            console.log(response);
            //var obj = JSON.parse(response);
            id = response["hashed_id"];

            //create the correct URL link.  Ricciwawa and Riccinalysis are different
            if (window.location.href.indexOf("riccinalysis")>0)
                $("#span_public_article_code").html('https://www.ricciwawa.com/riccinalysis?sc='+response["public_code"]);
            else
                $("#span_public_article_code").html('https://www.ricciwawa.com/?sc='+response["public_code"]);
            $("#div_public_article_code").show();
            ocr_sentence = "";
            json_file = id+".json"
            trans_audio_file = id+"_trans.mp3";
            eng_text = "";
            input_text= response['input_text']
            eng_spaced_sentence = response["eng_spaced_sentence"]
            public_code = response["public_code"]
            trans_meaning_word = response["trans_meaning_word"]
            trans_meaning_article = response["trans_meaning_article"]
            image_link = response ["image_link"]
            console.log(id)
            if (image_link != "") {
                $("#public_article_img").attr("src",image_link);
                $("#div_public_article_img").show();
            }
            $('#myModal').modal('hide');
            show_analyzed_text_trans(eng_spaced_sentence, trans_meaning_word, trans_meaning_article)
            $("#text_analysis").show();         
            for (var i = 0; i < 5; i++) {
                setTimeout(function(){
                    if (sessionStorage.getItem("trans_audio_download") != "done") {
                        $.ajax({
                            url: '/get_content?mp3=y&pc='+public_code,
                            type: 'GET',
                            contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                            processData: false, // NEEDED, DON'T OMIT THIS
                            // ... Other options like success and etc
                            success: function (response_check_file) { 

                              trans_audio_file = response_check_file["filename_trans_mp3"];
              
                                //check if response has a link, if so the file exists
                                if (trans_audio_file!=undefined) {
                                    $("#trans_audio_text").attr("src","data:audio/mp3;base64," + trans_audio_file);
                                    //set the session storage to done if files are downloaded successfully
                                    sessionStorage.setItem("trans_audio_download", "done");
                                    $("#div_audio").show()
                                }                            
                            }
                        })
                    }
                }, time_dalay[i]*1000)
            }                  
        },
        error: function(){
            alert('Error of processing the image.');
            $('#myModal').modal('hide')
        }
   });
}


//call TTS server
//a TTS server may take more than 1 minute to process the sentences.  Therefore, need to split into multiple smaller sentences
//But too many AJAX calls will overwhelm the TTS server
function create_svg_audio() {
    var form = $("#create_svg_audio")

    //text and image
    var formdata = new FormData(form[0]);
    var svg_formdata = {"inputtext":$("#inputtext").val(),"lang":$("#lang").val(),"index":0};
    var sentences = ($("#inputtext").val()).split(/(?=[。，.,]+)/);
    //$("#create_svg_audio_submit").prop('disabled', true);
    $('#myModal').modal('show')
    svg_formdata_ajax= new FormData();
    svg_formdata_ajax.append("text",$("#inputtext").val());
    time_dalay = [15,22,30,35,45,50,55]
    $("#translated_text").html("");
    $("#span_public_article_code").html("");
    $("#processed_text_analysis_text").html("");
    sessionStorage.setItem("mandarin_audio_download", "")
    sessionStorage.setItem("cantonese_audio_download", "")
    sessionStorage.setItem("text_analysis", "");
    sessionStorage.setItem("mandarin_audio_download", "");
    sessionStorage.setItem("cantonese_audio_download", "");
    $("#div_audio").hide()

    //list which characters belong to a sentence 
    $.ajax({      
        url: '/convert',
        //data: svg_formdata_ajax,
        data: formdata,
        type: 'POST',
        contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
        processData: false, // NEEDED, DON'T OMIT THIS
        success: function (response) { 
            console.log(response);
            //var obj = JSON.parse(response);
            id = response["hashed_id"];

            //create the correct URL link.  Ricciwawa and Riccinalysis are different
            if (window.location.href.indexOf("riccinalysis")>0)
                $("#span_public_article_code").html('https://www.ricciwawa.com/riccinalysis?sc='+response["public_code"]);
            else
                $("#span_public_article_code").html('https://www.ricciwawa.com/?sc='+response["public_code"]);
            $("#div_public_article_code").show();
            ocr_sentence = "";
            json_file = id+".json"
            cantonses_audio_file = id+"_trad.mp3";
            mandarin_audio_file = id+"_sim.mp3";
            sim_text = "";
            trad_text = "";
            sim_spaced_sentence = response["text_sim"]
            trad_spaced_sentence = response["text_trad"]
            pin_yin = response["pin_yin"]
            public_code = response["public_code"]
            english_meaning_word = response["english_meaning_word"]
            english_meaning_article = response["english_meaning_article"]
            image_link = response ["image_link"]
            console.log(id)
            if (image_link != "") {
                $("#public_article_img").attr("src",image_link);
                $("#div_public_article_img").show();
            }
            $('#myModal').modal('hide');
            show_analyzed_text(sim_spaced_sentence, trad_spaced_sentence, pin_yin, english_meaning_word, english_meaning_article)
            $("#text_analysis").show();         
            for (var i = 0; i < 5; i++) {
                setTimeout(function(){
                    if (sessionStorage.getItem("cantonese_audio_download") != "done" || sessionStorage.getItem("mandarin_audio_download") != "done") {
                        $.ajax({
                            url: '/get_content?mp3=y&pc='+public_code,
                            type: 'GET',
                            contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                            processData: false, // NEEDED, DON'T OMIT THIS
                            // ... Other options like success and etc
                            success: function (response_check_file) { 

                              cantonses_audio_file = response_check_file["filename_trad_mp3"];
                              mandarin_audio_file = response_check_file["filename_sim_mp3"];
              
                                //check if response has a link, if so the file exists
                                if (cantonses_audio_file!=undefined && mandarin_audio_file!=undefined) {
                                    $("#trad_audio_text").attr("src","data:audio/mp3;base64," + cantonses_audio_file);
                                    //set the session storage to done if files are downloaded successfully
                                    sessionStorage.setItem("cantonese_audio_download", "done");
                                    $("#sim_audio_text").attr("src","data:audio/mp3;base64," + mandarin_audio_file);
                                    //set the session storage to done if files are downloaded successfully
                                    sessionStorage.setItem("mandarin_audio_download", "done")
                                    $("#div_audio").show()
                                }                            
                            }
                        })
                    }
                }, time_dalay[i]*1000)
            }                  
        },
        error: function(){
            alert('Error of processing the image.');
            $('#myModal').modal('hide')
        }
   });
}

function progressHandler(event) {
  _("loaded_n_total").innerHTML = "Uploaded " + event.loaded + " bytes of " + event.total;
  var percent = (event.loaded / event.total) * 100;
  _("progressBar").value = Math.round(percent);
  _("status").innerHTML = Math.round(percent) + "% uploaded... please wait";
}

function completeHandler(event) {
  _("status").innerHTML = event.target.responseText;
  _("progressBar").value = 0;
}

function errorHandler(event) {
  _("status").innerHTML = "Upload Failed";
}

function abortHandler(event) {
  _("status").innerHTML = "Upload Aborted";
}      
//==============================================

//being called after audio loaded
function reload()
{
   audio_svg = document.getElementById("audio_svg");
   audio_svg.src=temp_base64[audio_playing_counter];
   audio_playing_counter = 0;
   audio_svg.onplay = function() {
      $("#error_msg").html(audio_playing_counter+" "+map_character_sentence[audio_playing_counter]);
      //highlight Chinese characters according to the position
      if ($("#lang").val()=="zh-mandarin" || $("#lang").val()=="zh" || $("#lang").val()=="zh-Hant") {
         $(".box").each(function() {
            temp_id =($(this)[0]).id;
            temp_id = temp_id.replace("box_","");
            //check if within the range
            if (parseInt(temp_id)>=map_character_sentence[audio_playing_counter][0] && parseInt(temp_id)<=map_character_sentence[audio_playing_counter][1]) {
               $(this)[0].style.backgroundColor = "#98fb98";
            }
            else
               $(this)[0].style.backgroundColor = "white";
            
         });
      }
      //highlight English words according to the position
      if ($("#lang").val()=="en" || $("#lang").val()=="uk-en") {
         $(".svg_span").each(function() {
            temp_id =($(this)[0]).id;
            temp_id = temp_id.replace("svg_span_","");
            //check if within the range
            if (parseInt(temp_id)==audio_playing_counter) {
               $(this)[0].style.backgroundColor = "#98fb98";
            }
            else
               $(this)[0].style.backgroundColor = "white";
            
         });
      }   
      
      audio_svg.play();
   };
   audio_svg.onended = function() {
      console.log("onended");
      setTimeout(function(){
         if (audio_playing_counter+1<temp_base64.length)
         {
            audio_playing_counter=audio_playing_counter+1;     
            audio_svg.src=temp_base64[audio_playing_counter];
            $("#error_msg").html("Playing audio "+audio_playing_counter);
            audio_svg.currentTime = 0.2;               
            audio_svg.play();
         }
      },1);  
   }   
   audio_svg.ontimeupdate = function() {
      if (audio_svg.currentTime<audio_svg.duration-0.5 && audio_svg.currentTime>audio_svg.duration-.8)
         audio_svg.currentTime = audio_svg.duration;
   };

   $('#audio_fast_backward_btn').click(function() {
      audio_playing_counter=0;
      $("#error_msg").html(audio_playing_counter);
      audio_svg.src=temp_base64[audio_playing_counter];
      audio_svg.currentTime = 0;
      audio_svg.play();
   })
   
   $('#audio_backward_btn').click(function() {
      if (audio_playing_counter-1<0) {
         audio_playing_counter=0;
      }
      else
         audio_playing_counter = audio_playing_counter - 1
      $("#error_msg").html(audio_playing_counter);
      audio_svg.src=temp_base64[audio_playing_counter];
      audio_svg.currentTime = 0;
      audio_svg.play();
   })
   $('#audio_forward_btn').click(function() {
      console.log("forward:" +audio_playing_counter);
      if (audio_playing_counter + 1 >= temp_base64.length) {
         console.log("forward:" + audio_playing_counter);
         audio_playing_counter = temp_base64.length - 1;
      } 
      else
         audio_playing_counter = audio_playing_counter + 1   
      $("#error_msg").html(audio_playing_counter);
      
      audio_svg.src=temp_base64[audio_playing_counter];     
      audio_svg.currentTime = 0;
      audio_svg.play();
   })   
   $('#audio_play_btn').click(function() {
      $("#error_msg").html(audio_playing_counter);   
      if (audio_svg.currentTime == audio_svg.duration || audio_svg.currentTime == pause_audio_time)
      {
         audio_svg.currentTime = 0;
         if (audio_playing_counter + 1 >= temp_base64.length) {
            audio_playing_counter = temp_base64.length - 1;
         } 
         audio_svg.src=temp_base64[audio_playing_counter];
      }
      else if (audio_svg.currentTime < 0.05)   
            audio_svg.currentTime = 0
         else
            audio_svg.currentTime = pause_audio_time;      
      //audio_svg.playbackRate  = 1;
      audio_svg.play();
   })
   $('#audio_pause_btn').click(function() {
      $("#error_msg").html(audio_playing_counter);
      pause_audio_time=audio_svg.currentTime
      audio_svg.pause();
   })  
}


//function load_text_show_modal
//load the text from selected cartoon
//show modal, choose picture, load the text and picture from the server and then show to the user
function load_text_from_cartoon()
{
   $('#myModal').modal('show')
   $('#loadModal').modal('show')
   load_text = [];
   $.ajax({
      url: '/load_text?useremail='+"kenneth00yip@gmail.com",
      type: 'GET',
      contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
      processData: false, // NEEDED, DON'T OMIT THIS
      // ... Other options like success and etc
      success: function (response) { 
         var obj = JSON.parse(response);
         console.log(obj);
         svg_output_html = ""
         group_counter=0;
         $('#myModal').modal('hide')
         for (var i in obj) {
            var current_id = obj[i].filename.replace("save_cartoon","");
            var current_lang = obj[i].lang;
            var current_content = obj[i].content;
            load_text.push( {id:current_id, lang:current_lang, content:current_content});
            $("#div_cartoon_text_"+current_id).html(current_content);
         }
      }
   })   
}

function load_text_to_textarea(cartoon_id)
{  
   id=cartoon_id.replace("load_cartoon","")
   for (var  i=0;i<load_text.length; i++) {
      if (id==load_text[i].id) {
         $("#inputtext").val(load_text[i].content);
         $('#loadModal').modal('hide');
      }
   }
}   

function show_story_entry(){
    $(".entry_story_group").show();
}

//function to allow to get the story code from thr URL
function check_url() {
    const queryString = window.location.search;
    console.log(queryString);
    const urlParams = new URLSearchParams(queryString);
    const storycode = urlParams.get('sc')
    console.log (storycode)
    //check if the story code is valid
    if (storycode != undefined) {
        if (storycode.length>23 && storycode.length<30) {        
            $("#input_article_code").val(storycode);
            code_entered();
            $(".entry_story_group").hide();
        }
    }
}
  
$(document).ready(function(){
   $('input[type="checkbox"]').change(function(){
       this.value = this.checked ? 1 : 0;
   });
   $('#input_image_file').on('change',function(event){
      $('#btn_submit').prop('disabled',false);
   })
   $('#nonchinese').change('change',function(event){
      if($(this).is(":checked")) {
         var inputtext_temp_hold = $("#inputtext").val()
         inputtext_temp_hold=inputtext_temp_hold.replace(/[a-zA-Z0-9äãāáǎ àōóǒòēéěèīíǐìūúǔùǖǘǚǜü\n]/g,'');
         $("#inputtext").val(inputtext_temp_hold)
      }

      $('#textbox1').val($(this).is(':checked'));        
    });
   $('.nav-link').click(function() {
      nav_bar_id = this.id;
      $( ".nav-link" ).each(function() {
         //console.log($(this)[0].id ,nav_bar_id)
         if ($(this)[0].id != nav_bar_id)
            $("#container_"+$(this)[0].id).css("display","none");
      });      
      $( "#container_"+nav_bar_id ).css("display","block");      
      $('.navbar-toggler').click()
      if (nav_bar_id != "nav_link_3")
         $(".audio_buttons").css("display", "none");
      else if (temp_base64.length >0) { //already has audio data
         $(".audio_buttons").css("display", "block");
      }
    }); 
   $("#notes").change('change',function(event) {
      if($(this).is(":checked")) {
         $(".box").css("height", "220px");
         $(".explain").css("display", "block");
      }
      else {
         $(".box").css("height", "300px");
         $(".explain").css("display", "none");
      }
   })
   
   $(".box").on('click',function(event){
      console.log($(this)[0].id);
   });   
   $(".group_box").on('click',function(event){
      console.log($(this)[0].id)
      id_name=($(this)[0].id).substring(6)
      console.log(term_explain [id_name]);
      alert(term_explain[id_name].term + ": "+term_explain[id_name].explain)
   });
   $("#clear_button").on('click',function(event){
      $("#input_article_code").val("")
      $("#inputtext").val("");
      $("#translated_text").html("");
      $("#span_public_article_code").html("");
      $("#processed_text_analysis_text").html("");
      $("#div_public_article_code").hide();
      $("#div_public_article_img").hide();
      $("#div_audio").hide();
      sessionStorage.setItem("text_analysis", "");
      sessionStorage.setItem("mandarin_audio_download", "")
      sessionStorage.setItem("cantonese_audio_download", "")
   })
   $(".load_cartoonlogo").on('click',function(event){
      load_text_to_textarea($(this)[0].id);
   })
   $(".save_cartoonlogo").on('click',function(event){
      save_text_to_cartoon($(this)[0].id);
   })   
   $("#retrive_text_btn").on('click',function(event){
      $('#loadModal').modal('show');
      load_text_from_cartoon()
   }) 
   $("#save_text_btn").on('click',function(event){
      $("#saveModal").modal('show');
   })    
})

window.addEventListener('load', function () {
    document.getElementById('sign-out').onclick = function () {
      firebase.auth().signOut();
    };
  
    // FirebaseUI config.
    var uiConfig = {
      signInSuccessUrl: '/',
      signInOptions: [
        // Comment out any lines corresponding to providers you did not check in
        // the Firebase console.
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID,
        //firebase.auth.FacebookAuthProvider.PROVIDER_ID,
        //firebase.auth.TwitterAuthProvider.PROVIDER_ID,
        //firebase.auth.GithubAuthProvider.PROVIDER_ID,
        //firebase.auth.PhoneAuthProvider.PROVIDER_ID
  
      ],
      // Terms of service url.
      tosUrl: '<your-tos-url>'
    };
  
    firebase.auth().onAuthStateChanged(function (user) {
      if (user) {
        // User is signed in, so display the "sign out" button and login info.
        document.getElementById('sign-out').hidden = false;
        document.getElementById('login-info').hidden = false;
        console.log(`Signed in as ${user.displayName} (${user.email})`);
        user.getIdToken().then(function (token) {
          // Add the token to the browser's cookies. The server will then be
          // able to verify the token against the API.
          // SECURITY NOTE: As cookies can easily be modified, only put the
          // token (which is verified server-side) in a cookie; do not add other
          // user information.
          document.cookie = "token=" + token;
        });
      } else {
        // User is signed out.
        // Initialize the FirebaseUI Widget using Firebase.
        try {
            var ui = new firebaseui.auth.AuthUI(firebase.auth());
            // Show the Firebase login button.
            ui.start('#firebaseui-auth-container', uiConfig);
        }
        catch {
            console.log("instance already created")
        }
        // Update the login state indicators.
        document.getElementById('sign-out').hidden = true;
        document.getElementById('login-info').hidden = true;
        // Clear the token cookie.
        document.cookie = "token=";
      }
    }, function (error) {
      console.log(error);
      alert('Unable to log in: ' + error)
    });

    $('#nav_link_2').click() 
  });
  
  function show_upload_image(img_file){
    var reader = new FileReader();
    
    reader.onload = function (e) {
        $('#show_upload_image').attr('src', e.target.result);
    }        
    reader.readAsDataURL(img_file);
  }

  firebase.auth().onAuthStateChanged((user) => {
    if (user) {
      // User is signed in, see docs for a list of available properties
      // https://firebase.google.com/docs/reference/js/firebase.User
      var uid = user.uid;
      console.log(uid)
      // ...
    } else {
      // User is signed out
      // ...
    }
  });
  
  $(function() {

    firebase.auth().signInAnonymously()
    .then(() => {
        console.log("signed in")
    })
    .catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
        // ...
    });

    // preventing page from redirecting
    $("html").on("dragover", function(e) {
        e.preventDefault();
        e.stopPropagation();
        $("h1").text("Drag here");
    });

    $("html").on("drop", function(e) { e.preventDefault(); e.stopPropagation(); });

    // Drag enter
    $('.div_image_upload-area-area').on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $("h1").text("Drop");
    });

    // Drag over
    $('.div_image_upload-area-area').on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $("h1").text("Drop");
    });

    // Drop
    $('.div_image_upload-area-area').on('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
        $("h1").text("Upload");

        var file = e.originalEvent.dataTransfer.files;
        var fd = new FormData();
        fd.append('input_image_file_b', file[0]);
        show_upload_image(fd)
    });

    // Open file selector on div click
    $("#div_image_upload-area").click(function(){
        $("#input_image_file_b").click();
    });

    // file selected
    $("#input_image_file_b").change(function(){
        var fd = new FormData();
        var files = $('#input_image_file_b')[0].files[0];
        fd.append('input_image_file_b',files);
        show_upload_image(files)
    });
    //$('.input-images').imageUploader();

    // Execute a function when the a story code is entered on the keyboard    
    document.getElementById("input_article_code").addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        code_entered();
        }
    });    

    //function to check if url has the story code
    check_url();
    $('#languge_selection').change(function() {
        if ($("#languge_selection").is(':checked')){
            $("#trad_audio_text").show();
            document.getElementById("sim_audio_text").pause();
            $("#sim_audio_text").hide();
            document.getElementById("trad_audio_text").play();

        }
        else{
            $("#trad_audio_text").hide();
            document.getElementById("trad_audio_text").pause();
            $("#sim_audio_text").show();
            document.getElementById("sim_audio_text").play();

        }
    })
    $('#nav_link_0').click(function(){ show_story_entry(); return false; });

});
