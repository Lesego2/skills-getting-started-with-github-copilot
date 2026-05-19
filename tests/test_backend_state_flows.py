def test_signup_then_get_activities_shows_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "flowstudent@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"
    activities_url = "/activities"

    # Act
    signup_response = client.post(signup_url, params={"email": email})
    activities_response = client.get(activities_url)

    # Assert
    assert signup_response.status_code == 200
    assert activities_response.status_code == 200
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_then_unregister_removes_participant(client):
    # Arrange
    activity_name = "Science Club"
    email = "flowremove@mergington.edu"
    signup_url = f"/activities/{activity_name}/signup"
    unregister_url = f"/activities/{activity_name}/signup"
    activities_url = "/activities"

    # Act
    signup_response = client.post(signup_url, params={"email": email})
    unregister_response = client.delete(unregister_url, params={"email": email})
    activities_response = client.get(activities_url)

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert activities_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]


def test_multiple_signups_for_same_activity_are_persisted(client):
    # Arrange
    activity_name = "Art Studio"
    emails = ["one@mergington.edu", "two@mergington.edu"]
    signup_url = f"/activities/{activity_name}/signup"
    activities_url = "/activities"

    # Act
    first_response = client.post(signup_url, params={"email": emails[0]})
    second_response = client.post(signup_url, params={"email": emails[1]})
    activities_response = client.get(activities_url)

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 200
    participants = activities_response.json()[activity_name]["participants"]
    assert emails[0] in participants
    assert emails[1] in participants