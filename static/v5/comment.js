$(document).ready(function() {
    $('#form_comment_post').on('submit', function (e) {
        e.preventDefault();
        commment = $("#commment").val();
        if (commment == "") {
            alert("Please enter your content here");
        } else {
            //user_id = uid;
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const storycode = urlParams.get('sc');

            //datatime
            var today = new Date();
            var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            var dateTime = date + ' ' + time;

            //get primary key
            comment_id = storycode + Math.random() * 10;
            var form = $("#form_comment_post")
            var formdata = new FormData(form[0]);
            formdata.append("sc", storycode);

            $.ajax({
                url: '/post_comments',
                data: formdata,
                type: 'POST',
                contentType: false, // NEEDED, DON'T OMIT THIS (requires jQuery 1.6+)
                processData: false, // NEEDED, DON'T OMIT THIS
                success: function (response) { 
                    console.log(response);
                }
            })                    
        }


    });


    firebase.auth().onAuthStateChanged((user) => {
        // first check user login or not 
        if (user) {
            var user_id = user.uid;
        } else {
            var user_id = 0;
        }

        //replay data insert into the database
        $(".reply-message").click(function() {
            $(this).next('.form').toggle('swing');
            var replay_id = $(this).attr('value');
            $(".form").submit(function(e) {
                e.preventDefault();
                //repaly_commment = $(".form textarea").val();
                var replay_commment = "";
                jQuery("textarea#repaly_commment").each(function() {
                    replay_commment += jQuery(this).val() + "\n";
                });
                if (replay_commment == "") {
                    alert("Please enter your content here");
                } else {
                    //user_id = uid;
                    const queryString = window.location.search;
                    const urlParams = new URLSearchParams(queryString);
                    const storycode = urlParams.get('sc');

                    //datatime
                    var today = new Date();
                    var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
                    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
                    var dateTime = date + ' ' + time;

                    //get primary key
                    comment_id = storycode + Math.random() * 10;
                    var data = {
                            user_id: user_id,
                            storycode: storycode,
                            parent_comment_id: replay_id,
                            comment_id: comment_id,
                            commment: replay_commment,
                            datetime: dateTime

                        }
                        // Get a reference to the database service
                    var database = firebase.database();
                    //get last row
                    var query = firebase.database().ref("comments").orderByKey().limitToLast(1);
                    query.once("value")
                        .then(function(snapshot) {
                            snapshot.forEach(function(childSnapshot) {
                                // key will be "ada" the first time and "alan" the second time
                                let key = childSnapshot.key;
                                if (key == "") {
                                    row_id = "0";
                                } else {
                                    row_id = +key + 1;
                                }
                                var ref = database.ref("comments/" + row_id).set(data);
                                if (ref) {
                                    tinymce.activeEditor.setContent('');
                                    $(".user-comment-section").after().append('<li class="admin-comment-box"><img src="../static/img/default.png" class="user-image" alt=""><textline class="content">' + replay_commment + '</textline><p class="time-date">' + dateTime + '</p><div class="love Addto-playlist" title="Likes:7868"><i class="fas fa-heart"></i><span>liked!</span></div><span class="reply-message replay" id="replay" value="{{ comment_data["' + comment_id + '"] }}">Reply</span> <form class="form" method="POST"><textarea name="commment" id="repaly_commment"></textarea><button name="submit" class="comment-btn">Comment</button></form></li>');
                                    $('.form').each(function() {
                                        $(this).hide();
                                    });

                                } else {
                                    alert("There have a problem");
                                }
                            });
                        });
                }

            });

        });



        /* Likes and Dislike function */
        $(".commment-section .user-comment-section .love i").on("click", function() {
            var like_id = $(this).attr("id");
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const storycode = urlParams.get('sc');

            //datatime
            var today = new Date();
            var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            var dateTime = date + ' ' + time;

            var database = firebase.database();
            //database.ref("comment_like").push(data);
            firebase.database().ref("comment_like").orderByChild("comment_id").equalTo(like_id).once('child_added', function(snapshot) {
                var storycode_liked = snapshot.val().storycode;
                var like_comment_id = snapshot.val().comment_id;
                var like_user_id = snapshot.val().user_id;
                alert(like_user_id);
                alert(user_id);

                if (like_id == like_comment_id && storycode == storycode_liked && user_id == like_user_id) {
                    //if alread like exit then update table
                    alert(user_id);
                    snapshot.ref.remove();
                } else {
                    //if like dose not exists then insert like

                    var data = {
                        user_id: user_id,
                        storycode: storycode,
                        comment_id: like_id,
                        comment_like: "like",
                        datetime: dateTime
                    }

                    var ref = database.ref("comment_like").push(data);
                    if (ref) {
                        firebase.database().ref("comments").orderByChild("comment_id").equalTo(like_id).once('child_added', function(snapshot) {
                            var storycode_liked = snapshot.val().storycode;
                            var like_comment_id = snapshot.val().comment_id;
                            let count_like = snapshot.val().like;
                            var like = +count_like + 1;
                            if (like_id == like_comment_id && storycode == storycode_liked) {
                                //if alread like exit then update table
                                snapshot.ref.update({ like: like });
                            }
                        });
                    }
                }
            });

        });

        $(".commment-section .user-comment-section .love i").each(function() {
            //$(this).next("span").toggleClass("press", 1500);
            $(this).addClass("press");
        });

    });





    //fetch firebase data orginal
    /*
     function addItemsToList(comment) {
         var ul = document.getElementById("user-comment-section");
         $(ul).append('<li class="user-comment-box"><img src="../static/img/default.png" class="user-image" alt=""><textline class="content">' + comment + '</textline><p class="time-date">2020-1220 14:15</p><div class="love Addto-playlist" title="Likes:7868"><i class="fas fa-heart"></i><span>liked!</span></div></li>');
     }

     function fetchData() {
         const queryString = window.location.search;
         const urlParams = new URLSearchParams(queryString);
         const storycode = urlParams.get('sc');
         firebase.database().ref("comments").orderByChild("storycode").equalTo(storycode).once('value', function(snapshot) {
             snapshot.forEach(
                 function(ChildSnapshot) {
                     let comment = ChildSnapshot.val().commment;

                     addItemsToList(comment)

                 }
             );
         });
     }
     */

    //fetchData();


});