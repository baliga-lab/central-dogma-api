(function (glob) {
    "use strict";
    // **********************************************************************
    // ****** Public API
    // **********************************************************************
    var cdapi = { };
    cdapi.version = '1.0.0';
    const BASE_URL = 'http://localhost:5000';
    //const BASE_URL = '/api';

    /* Get the session id */
    function get(name) {
        if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
            return decodeURIComponent(name[1]);
    }

    cdapi.getSessionID = function() {
        return get('sessionid');
    };
    cdapi.init = function() {
        console.log('this is the CD API: ' + cdapi.getSessionID());
    };

    cdapi.info = function() {
        const xhr = new XMLHttpRequest();
        const url = BASE_URL + "/info";
        fetch(url).then(function(response) { return response.json() })
            .then(function(jsonObj) {
                console.log(jsonObj);
            });
    };

    function postJSON(url, data) {
        return fetch(url, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json',
            },
            redirect: 'follow',
            referrer: 'no-referrer',
            body: JSON.stringify(data),
        }).then(response => response.json());
    }
    function postJSONAuth(url, data) {
        return fetch(url, {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + window.localStorage.getItem("loginToken")
            },
            redirect: 'follow',
            referrer: 'no-referrer',
            body: JSON.stringify(data),
        }).then(response => response.json());
    }
    function patchJSONAuth(url, data) {
        return fetch(url, {
            method: 'PATCH',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + window.localStorage.getItem("loginToken")
            },
            redirect: 'follow',
            referrer: 'no-referrer',
            body: JSON.stringify(data),
        }).then(response => response.json());
    }

    async function getAuth(url) {
        let headers = {"Authorization": "Bearer " + window.localStorage.getItem("loginToken")};
        const response = await fetch(url, {headers});
        return await response.json();
    }

    // These are the official API functions
    cdapi.register = async (username, password, grade, gender) => {
        return await postJSON(BASE_URL + "/user/register",
                              {"username": username, "password": password,
                               "grade": grade, "gender": gender}).then(data => {
                                   if (data.status == "ok") {
                                       window.localStorage.setItem("loginToken", data.access_token);
                                   }
                                   return data;
                               });
    };
    cdapi.login = async (username, password) => {
        return await postJSON(BASE_URL + "/user/login",
                              {"username": username, "password": password}).then(data => {
                                  if (data.status == "ok") {
                                      window.localStorage.setItem("loginToken", data.access_token);
                                  }
                                  return data;
                              });
    };

    cdapi.globalLeaderboard = async () => {
        const url = BASE_URL + "/leaderboard";
        const response = await fetch(url);
        return await response.json();
    };
    cdapi.sessionLeaderboard = async (sessionId) => {
        const url = BASE_URL + "/leaderboard/" + sessionId;
        const response = await fetch(url);
        return await response.json();
    };
    cdapi.sessionInfo = async (sessionId) => {
        return await getAuth(BASE_URL + "/session/" + sessionId);
    };
    cdapi.makeSession = async (sessionCode, startTime, endTime) => {
        return await postJSONAuth(BASE_URL + "/session",
                                  {"session_code": sessionCode, "start_time": startTime, "end_time": endTime});
    };
    cdapi.ownedSessions = async () => {
        return await getAuth(BASE_URL + "/session");
    };
    cdapi.modifySession = async (sessionCode, startTime, endTime) => {
        return await patchJSONAuth(BASE_URL + "/session/" + sessionCode,
                                   {"start_time": startTime, "end_time": endTime});
    };
    cdapi.userGames = async () => {
        return await getAuth(BASE_URL + "/game");
    };
    cdapi.logLevelCompletion = async (levelId, params) => {
        return await postJSONAuth(BASE_URL + "/game/" + levelId, params);
    };
    cdapi.logQuestionResponse = async (questionId, answerOption, correctness, sessionCode) => {
        return await postJSONAuth(BASE_URL + "/response/" + questionId,
                                  {'session_code': sessionCode,
                                   'correctness': correctness,
                                   'answer_option': answerOption});
    };
    cdapi.gameCompletionInfo = async () => {
        return await getAuth(BASE_URL + "/game");
    };

    // These lines needed to support a NPM/ES6 environment, the define() call
    // is to support RequireJS
    glob.cdapi = cdapi;
    typeof module != 'undefined' && module.exports ? module.exports = cdapi : typeof define === "function" && define.amd ? define("cdapi", [], function () { return cdapi; }) : glob.cdapi = cdapi;
})(typeof window != "undefined" ? window : this);
