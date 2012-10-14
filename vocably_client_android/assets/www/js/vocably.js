/*
   Main application logic
 */


$(document).ready(function() {
    //startApp after device ready
    //document.addEventListener("deviceready", startApp, false);
    startApp();
});


function init() {
    $.mobile.allowCrossDomainPages = true;
    $.support.cors = true;
};
 
function startApp() {
    init();
    
    // test ChildBrowser
    //window.plugins.childBrowser.showWebPage("http://en.wikipedia.org/wiki/Nietzsche", { showLocationBar: true, showNavigationBar: true, showAddress: true});
    
    // open childBrowser to perform Google Authentication, then get access token
    // then do what with access token? Get mail or send token to server and let server fetch mail?
    //var oAuth = liquid.helper.oauth;
    $("#access-code").click(function(event) {
        //liquid.helper.oauth.authorize(authorizeWindowChange);
        gotoPageWordlist();
        event.preventDefault();
    });
    //if (oAuth.isAuthorized()) {
    //    gotoPageWordlist();
    //}
    
}

function gotoPageWordlist() {
    $.mobile.changePage("#page-wordlist", {
        transition : "none",
    });
}

function gotoPageHome() {
    $.mobile.changePage("#page-unauthorized", {
        transition : "none",
        reverse: false,
        changeHash: false
    });
}


function authorizeWindowChange(uriLocation) {
    //console.log("Location Changed: " + uriLocation);
    var oAuth = liquid.helper.oauth;

    // oAuth process is successful!
    if (oAuth.requestStatus == oAuth.status.SUCCESS) {
        var authCode = oAuth.authCode;

        // have the authCode, now save the refreshToken and start Page TaskList
        oAuth.saveRefreshToken(
            { auth_code: oAuth.authCode}, 
            function() {
                gotoPageWordlist();
            }
        );
    }
    else if (oAuth.requestStatus == oAuth.status.ERROR) {
        console.log("ERROR - status received = oAuth.status.ERROR");
    }
}



(function() {
    $('#page-wordlist').live('pageshow', function(event) {
        // go back home page if not authorized
        //if (!liquid.helper.oauth.isAuthorized()) {
        //    gotoPageHome();
        //    return;
        //}

        // fetch words on loading of this page
        getWords();

        // listen for refresh button click
        $('#head-menu-refresh').click(function(event) {
            getWords();
            event.preventDefault();
        });
    });
})();


// get words json from server.
function getWords() {
    $.ajax({
        url: 'http://localhost:8080/words.json',
        dataType: 'json',
        success: function(data) {
            $("#wordlist").html('');
            $.each(data, function(word, definition) {
                $("#wordlist").append(
                    '<div data-role="collapsible" class="collapsible">'+
                        '<h3>'+word+'</h3>'+
                        '<p>'+definition+'</p>'+
                        '</div>'
                );
            });
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('getWords() failed');
        }
    });
};
