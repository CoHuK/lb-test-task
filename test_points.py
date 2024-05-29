from datetime import datetime
import requests

#eoracle has a points system, this system gives points (aka credit) to operators, stakers how locked their restaked ETH on eoracle.
# Operator is an entity (represented by an address in ethereum) that registerd to EigenLayer and then to eoracle as oeprator. Operators operate the eoracle protocol by running the software.
# Stakers are entities (represented by addresses in etheruem) who have money (ETH, LSTs, …) and the delegate the money to operators. 
# The points system credit the operators and stakers by the amount of money that they staked on eoracle.
# A Staker receives 1 point per hour based on the 1 ETH that was delegated to operator(s) that are registered to eoracle
# An Operator receives 1 points per hour based on 3% of the total ETH that was delegated to it by stakers.
# The points system is live and can be seen here - https://eo.app
# The points system has a backend process that runs every 10 minutes and collect the list of operators, and stakers (by looking on delegation and undelegation events) and calculate the total points to these addresses 
# The point system has also an api that one can use and get the points to a specific address https://eo.app/api/v1/points/<address>


API_ENDPOINT = "https://eo.app/api/v1/points/"
OPERATOR_TEST_ADDRESS = "0xF0452F2D9758EC02373612F5F1A83bbd3fF66e5d"
OPERATOR_START_POINT = {
"date": "2024-05-28T11:14:47.640Z",
"points": "777.3855136005855",
"stake": "32.01066960949819"
}
STAKER_TEST_ADDRESS = "0xc12A1D786922E727d07C34F27d555175A55f7461"
STAKER_START_POINT = {
"date": "2024-05-28T11:14:27.273Z",
"points": "21019.486092380892",
"stake": "32.01066960949819"
}



def get_hours_difference(date1, date2):
    # Parse the date strings into datetime objects
    d1 = datetime.fromisoformat(date1.replace("Z", "+00:00"))
    d2 = datetime.fromisoformat(date2.replace("Z", "+00:00"))

    # Calculate the difference in microseconds
    diff_seconds = (d2 - d1).total_seconds()

    # Convert seconds to hours
    diff_hours = diff_seconds / 3600

    return diff_hours

def test_get_points():
    response = requests.get(API_ENDPOINT + OPERATOR_TEST_ADDRESS)
    assert response.status_code == 200
    parsed_response =  response.json()
    today = datetime.now().date().isoformat()
    assert today in parsed_response["date"]
    assert float(parsed_response["points"]) > float(OPERATOR_START_POINT["points"])
    assert parsed_response["stake"] == OPERATOR_START_POINT["stake"]

def test_staker_points_calculation():
    response = requests.get(API_ENDPOINT + STAKER_TEST_ADDRESS)
    parsed_response =  response.json()
    last_points_date = parsed_response["date"]
    hours_difference = get_hours_difference(STAKER_START_POINT["date"], last_points_date)
    assert float(parsed_response["points"]) == (float(STAKER_START_POINT["points"]) + hours_difference * float(STAKER_START_POINT["stake"]))

def test_operator_points_calculation():
    response = requests.get(API_ENDPOINT + OPERATOR_TEST_ADDRESS)
    parsed_response =  response.json()
    last_points_date = parsed_response["date"]
    hours_difference = get_hours_difference(OPERATOR_START_POINT["date"], last_points_date)
    expected_points = float(OPERATOR_START_POINT["points"]) + hours_difference * float(OPERATOR_START_POINT["stake"]) * 0.03
    assert float(parsed_response["points"]) == expected_points