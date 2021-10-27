var inputtext_temp_hold=""
var audio_playing_counter = 0;
var audio_svg = document.getElementById("audio_svg");
var pause_audio_time=0;
var load_text = [];
//近年は毎年のように、全国で広範囲にわたる水害の被害が発生。さらに今年は新型コロナウイルスの感染が拡大する中、安全に避難するにはどうしたらいいか、一人一人が事前に考える必要性が高まっています。水害から、自分の命、そして大切な人の命を守るためにできることを、さまざまな角度から考えます。


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
//write to div processed_text_analysis_text
function show_analyzed_text(json_data){
    span_text =""
    $("#processed_text_analysis_text").html("")
    for (var char of json_data){
        word = char["k"]
        eng_word_defn = char["m"]
        symbol = char["s"]
        word_len = char["k"].length
        //a new text
        span_text = span_text + "<span class='span_char' style='width:"+ (word_len+1) + "em'><p class='span_p_char'>" + symbol + "</p>" + word + "</span>"
    }
    $("#processed_text_analysis_text").html(span_text)
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
   var form = $("#photoform")
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
  //ajax.upload.addEventListener("progress", progressHandler, false);
  //ajax.addEventListener("load", completeHandler, false);
  //ajax.addEventListener("error", errorHandler, false);
  //ajax.addEventListener("abort", abortHandler, false);
  //ajax.open("POST", "http://learningocr-177310.appspot.com/sign");
  //ajax.send(formdata);
}

function call_tts_ajax (i,formdata,sentences) {
   console.log(i,sentences[i])
   formdata.index=i;
   formdata.inputtext=sentences[i];
   formdata_ajax = new FormData();
   formdata_ajax.append("text",sentences[i]);
   formdata_ajax.append("index",i);
   formdata_ajax.append("lang",$("#lang").val());
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


//call JS TTS server
//a TTS server may take more than 1 minute to process the sentences.  Therefore, need to split into multiple smaller sentences
//But too many AJAX calls will overwhelm the TTS server
function create_svg_audio_jp() {
   $('#myModal').modal('show')
   $("#read_aloud_jp_div").hide()
   svg_formdata_ajax= new FormData();
   svg_formdata_ajax.append("text",$("#inputtext").val());
   
   time_dalay = [5,9,13,18,25,35]
   sessionStorage.setItem("text_analysis", "");
   sessionStorage.setItem("jp_audio_download", "");
   //list which characters belong to a sentence 
   $.ajax({
      //url: '/convertconvert',
      url: '/convertjp',
      data: svg_formdata_ajax,
      type: 'POST',
      contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
      processData: false, // NEEDED, DON'T OMIT THIS
      success: function (response) { 
         console.log(response);
         var obj = response;
         id = obj["id"];

         ocr_sentence = "";
         json_file = id+".json"
         jp_audio_file = id+"_jp.mp3";
         jp_text = "";
         jp_spaced_sentence = ""
         console.log(id)
         for (var i = 0; i < 5; i++) {
            setTimeout(function(){
               if (sessionStorage.getItem("text_analysis") != "done") {
                  $.ajax({
                     url: '/check_file?file_name='+json_file,
                     type: 'GET',
                     contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                     processData: false, // NEEDED, DON'T OMIT THIS
                     // ... Other options like success and etc
                     success: function (response_check_file) { 
                        //check if response has yes, if so the file exists
                        if (response_check_file == "yes\n") {
                           $.ajax({
                              url: '/get_json?json_id='+json_file,
                              type: 'GET',
                              contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                              processData: false, // NEEDED, DON'T OMIT THIS
                              // ... Other options like success and etc
                              success: function (response_json) { 
                                 console.log(response_json)
                                 //$("#text_analysis_text").html(JSON.stringify(response_json));
                                 //set the session storage to done if files are downloaded successfully
                                 sessionStorage.setItem("text_analysis", "done");
                                 //$('#nav_link_3').click() //goto to audio
                                 $('#myModal').modal('hide');
                                 show_analyzed_text(response_json)
                                 $("#text_analysis").show();
                              }
                           })
                        }
                     }
                  })
               }

               if (sessionStorage.getItem("jp_audio_download") != "done") {
                  $.ajax({
                     url: '/check_file?file_name='+jp_audio_file,
                     type: 'GET',
                     contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                     processData: false, // NEEDED, DON'T OMIT THIS
                     // ... Other options like success and etc
                     success: function (response_check_file) { 
                        //check if response has yes, if so the file exists
                        if (response_check_file == "yes\n") {
                           $("#jp_audio_text").attr("src","/get_audio?audio_id="+jp_audio_file);
                           //set the session storage to done if files are downloaded successfully
                           sessionStorage.setItem("jp_audio_download", "done");
                           $("#read_aloud_jp_div").show()
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
   var formdata = {"inputtext":$("#inputtext").val(),"lang":$("#lang").val(),"index":0};
   var svg_formdata = {"inputtext":$("#inputtext").val(),"lang":$("#lang").val(),"index":0};
   var sentences = ($("#inputtext").val()).split(/(?=[。，.,]+)/);
   //$("#create_svg_audio_submit").prop('disabled', true);
   $('#myModal').modal('show')
   svg_formdata_ajax= new FormData();
   svg_formdata_ajax.append("text",$("#inputtext").val());
   time_dalay = [5,7,10,14,17,22,30,35,45,50,55]
   sessionStorage.setItem("text_analysis", "");
   sessionStorage.setItem("mandarin_audio_download", "");
   sessionStorage.setItem("cantonese_audio_download", "");
   //list which characters belong to a sentence 
   $.ajax({
      //url: '/convertconvert',
      url: '/convertjp',
      data: svg_formdata_ajax,
      type: 'POST',
      contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
      processData: false, // NEEDED, DON'T OMIT THIS
      success: function (response) { 
         console.log(response);
         var obj = JSON.parse(response);
         id = obj["id"];

         ocr_sentence = "";
         json_file = id+".json"
         cantonses_audio_file = id+"_trad.mp3";
         mandarin_audio_file = id+"_sim.mp3";
         sim_text = "";
         trad_text = "";
         sim_spaced_sentence = ""
         trad_spaced_sentence = ""

         console.log(id)
         for (var i = 0; i < 10; i++) {
            setTimeout(function(){
               if (sessionStorage.getItem("text_analysis") != "done") {
                  $.ajax({
                     url: '/check_file?file_name='+json_file,
                     type: 'GET',
                     contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                     processData: false, // NEEDED, DON'T OMIT THIS
                     // ... Other options like success and etc
                     success: function (response_check_file) { 
                        //check if response has yes, if so the file exists
                        if (response_check_file == "yes\n") {
                           $.ajax({
                              url: '/get_json?json_id='+json_file,
                              type: 'GET',
                              contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                              processData: false, // NEEDED, DON'T OMIT THIS
                              // ... Other options like success and etc
                              success: function (response_json) { 
                                 console.log(response_json)
                                 //$("#text_analysis_text").html(JSON.stringify(response_json));
                                 //set the session storage to done if files are downloaded successfully
                                 sessionStorage.setItem("text_analysis", "done");
                                 //$('#nav_link_3').click() //goto to audio
                                 $('#myModal').modal('hide');
                                 show_analyzed_text(response_json)
                                 $("#text_analysis").show();
                              }
                           })
                        }
                     }
                  })
               }

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
                           $("#trad_audio_text").attr("src","/get_audio?audio_id="+cantonses_audio_file);
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
                           $("#sim_audio_text").attr("src","/get_audio?audio_id="+mandarin_audio_file);
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

function save_text_to_cartoon (id)
{
   savetext_formdata_ajax= new FormData();
   savetext_formdata_ajax.append("content",$("#inputtext").val());
   savetext_formdata_ajax.append("useremail","kenneth00yip@gmail.com");
   savetext_formdata_ajax.append("lang",$("#lang").val());      
   savetext_formdata_ajax.append("filename",id);      
   $.ajax({
      url: '/save_text',
      data: savetext_formdata_ajax,
      type: 'POST',
      contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
      processData: false, // NEEDED, DON'T OMIT THIS
      // ... Other options like success and etc
      success: function (response) { 
         var result = response;
         console.log(result);
         if (result==0)
            alert ("Successfully saved");
         else
            alert ("Erros. Not saved.");
         $("#saveModal").modal('hide');
      }
   })
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
      $("#inputtext").val("");
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
        var ui = new firebaseui.auth.AuthUI(firebase.auth());
        // Show the Firebase login button.
        ui.start('#firebaseui-auth-container', uiConfig);
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
  