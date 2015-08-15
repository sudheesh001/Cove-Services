# Cove-Services
Leaderboard, registration and score services for the cove game built with Unity. This is the cloud service API endpoints of the application


# API Endpoints

request to `url/` results in the leaderboard response
```
[{"username": "<username1>", "idLeaderboard": 2, "score": "10"}, {"username": "<username2>", "idLeaderboard": 1, "score": "0"}]
```

To add a new user sent a GET / POST request to `/add/<username>` it'll create an object like this, 0 starting score
```
{"username": "<new username>", "idLeaderboard": "<new id>", "score": "0"}
```

To update the username record do send a request to `/update/<username>/<score>` with new score
the response will be
```
{"success": "True"}
```
if the score is updated correctly, then send a request back to `url/` to get the updated leaderboard