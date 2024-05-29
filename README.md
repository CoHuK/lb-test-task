# LB Test task

The latest Allure report is available here: [Allure](https://cohuk.github.io/lb-test-task)

## Test Plan

### Goal

To ensure the accuracy, reliability, and robustness of the system that credits points to operators and stakers based on their staked assets.

### Scope

* DApp with API interface at https://eo.app/api/v1/. All the endpoints available
* DApp scheduler (timely execution)
* Smart contract's available actions. [Version XX] (Calculations, points transactions)

### Objectives

* Verify that the points calculations for both stakers and operators are precise according to the rules specified
* Ensure the backend process updates points every 10 minutes as expected
* Handle edge cases like simultaneous delegation/undelegation, operators or stakers with zero balance, and unexpected system inputs.

### Test items

* Points Calculation: Ensure all formulas for point calculations are tested
* Data Integration: Verify correct data handling from blockchain events to system database
* API Endpoints: Validate all API endpoints for fetching and updating point balances
* Smart contract methods: Validate all methods available on the smart contract

### Approach

#### Testing strategy

* Implement JS tests with web3 library to interact with smart contract. Jest framework.
* Implement unit tests for the DApp. (Define coverage %% and modules for mandatory coverage) Framework will be chosen based on the programming language used for the DApp
* Implement integration tests for Dapp/DB communication. PyTest framework
* Implement system tests to verify API endpoints and DApp functionality. PyTest framework + 'requests' lib

Only functional testing will be performed in this test round. Security, Usability and Performance tests will be designed separately if required.

### Acceptance criteria

* No issues with the calculation logic and functionality
* Scheduler issues could be deprioritised after approval of the product owner
* All the tests are implemented and 100% green

### Testing process

* Test cases implementation for integration and system tests
* Tests execution
* Unit tests implementation
* Integration/system tests implementation
* CI setup for tests execution
* Addition of implemented tests into regression suite
* Addition of critical tests into smoke/monitoring suites

Issues will be reported into the task tracker with label "Points_calculation" into the current sprint

### Artefacts

* Test Plan
* Test Cases (in TMS)
* Test scripts (repo, branch "XXX")
* Test report will be sent by QA Lead to all stakeholders and published in TMS
* Test completion report will be attached to the current Test Plan

### Environment

* The first round of tests will be performed on the testnet
* Production testing will be done after the release

### Risks

Do be set with product owner.
Possible risks:
* blockchain network instability
* high gas prices affecting smart contract interactions
* resources unavailability
* ...

### Schedule

* Unit tests coverage: by xx/xx/xx
* Test cases implementation: by xx/xx/xx
* Tests scripts implementation: by xx/xx/xx
* First round of test execution: by xx/xx/xx
* Bug fixing period: 2 days
* Second round of test execution: by yy/yy/yy
* Release planned date: zz/zz/zz
* Production testing: after release deployment

### Approvals

* QA Lead
* Product owner
* CTO

Sign offs are to be done in the release ticket http://jira
