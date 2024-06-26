from datetime import datetime
import requests
import allure

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


@allure.step("Get the hours difference between two dates")
def get_hours_difference(date1, date2):
    d1 = datetime.fromisoformat(date1.replace("Z", "+00:00"))
    d2 = datetime.fromisoformat(date2.replace("Z", "+00:00"))

    diff_seconds = (d2 - d1).total_seconds()
    diff_hours = diff_seconds / 3600

    return diff_hours

@allure.step("Get points for address")
def get_points_for_address(address):
    response = requests.get(API_ENDPOINT + address)
    assert response.status_code == 200
    return response.json()

@allure.title("Test points getter request")
@allure.description("Test that the points getter request returns 200 status code and has the correct data structure")
def test_get_points():
    parsed_response =  get_points_for_address(OPERATOR_TEST_ADDRESS)
    today = datetime.now().date().isoformat()
    assert today in parsed_response["date"]
    assert float(parsed_response["points"]) > float(OPERATOR_START_POINT["points"])
    assert parsed_response["stake"] == OPERATOR_START_POINT["stake"]

@allure.title("Test Staker points calculation")
@allure.description("Test that the staker points are calculated correctly based on the staker's stake and the time passed since the last points calculation\nThe staker receives 1 point per hour based on the 1 ETH that was delegated to operator(s) that are registered to eoracle")
def test_staker_points_calculation():
    parsed_response =  get_points_for_address(STAKER_TEST_ADDRESS)
    last_points_date = parsed_response["date"]
    hours_difference = get_hours_difference(STAKER_START_POINT["date"], last_points_date)
    assert float(parsed_response["points"]) == (float(STAKER_START_POINT["points"]) + hours_difference * float(STAKER_START_POINT["stake"]))

@allure.title("Test Operator points calculation")
@allure.description("Test that the operator points are calculated correctly based on the operator's stake and the time passed since the last points calculation\nThe operator receives 1 points per hour based on 3% of the total ETH that was delegated to it by stakers.")
def test_operator_points_calculation():
    parsed_response =  get_points_for_address(OPERATOR_TEST_ADDRESS)
    last_points_date = parsed_response["date"]
    hours_difference = get_hours_difference(OPERATOR_START_POINT["date"], last_points_date)
    expected_points = float(OPERATOR_START_POINT["points"]) + hours_difference * float(OPERATOR_START_POINT["stake"]) * 0.03
    assert float(parsed_response["points"]) == expected_points