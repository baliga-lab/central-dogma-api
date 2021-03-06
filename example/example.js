cdapi.info();
/*
  cdapi.register("user", "password", 6, "m").then(result => {
  console.log("register result");
  console.log(result);
  }); */
cdapi.login("user", "password").then(result => {
    console.log('logged in');
    /*
    cdapi.logLevelCompletion("level1", {"score": 12345}).then(data => {
      console.log("log level completion (no session)")
      console.log(data);
    });
*/
    cdapi.levelData("level1", {}).then(data => {
      console.log("level data (no session)")
      console.log(data);
    });
    /*
      cdapi.makeSession("session1", "2019-08-15 12:00:00", "2019-08-20 12:00:00").then(data => {
      console.log("MAKE SESSION");
      console.log(data);
      });
      cdapi.ownedSessions().then(data => {
      console.log(data);
      });
      cdapi.sessionInfo("session1").then(data => {
      console.log(data);
      });
      cdapi.modifySession("session1", "2019-08-15 15:00:00", "2019-08-22 13:00:00").then(data => {
      console.log("MODIFY SESSION");
      console.log(data);
      });
      cdapi.logLevelCompletion("level1", {"score": 12345}).then(data => {
      console.log("log level completion (no session)")
      console.log(data);
      });
      cdapi.logLevelCompletion("level1", {"score": 12345, "session_code": "session1"}).then(data => {
      console.log("log level completion (with session)")
      console.log(data);
      });
      cdapi.logQuestionResponse("question1", "option1", 1, "session1").then(data => {
      console.log("log question response")
      console.log(data);
      });
    cdapi.logQuestionResponse("question1", "option1", 1, null).then(data => {
        console.log("log question response")
        console.log(data);
    });
    */
    /*
      cdapi.gameCompletionInfo().then(data => {
      console.log("game completion")
      console.log(data);
      }); */
    /*
      cdapi.logHyperlinkVisited('http://www.example.com').then(data => {
      console.log('hyperlink visited');
      console.log(data);
      });*/
}).catch(function() {
    console.log("can't log in");
});

cdapi.globalLeaderboard('name').then(leaderboard => {
    console.log('All time leaderboard');
    console.log(leaderboard);
});
cdapi.sessionLeaderboard('session1').then(leaderboard => {
    console.log('session leaderboard');
    console.log(leaderboard);
});

cdapi.levelGlobalLeaderboard('level1', 'name').then(leaderboard => {
    console.log('All time leaderboard');
    console.log(leaderboard);
});

cdapi.levelSessionLeaderboard('session1', 'level1', 'name').then(leaderboard => {
    console.log('Level session leaderboard');
    console.log(leaderboard);
});
