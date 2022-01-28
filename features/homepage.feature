Feature: The homepage

    @fixture.test_trello_board
    @fixture.test_app
    Scenario: visit the homepage
        When I go to the home page
        Then I should see "Current item storage method: Session"

    @fixture.test_trello_board
    @fixture.test_app
    Scenario: switch storage methods
        When I go to the home page
        and I click the "Switch backend" button
        Then I should see "Current item storage method: Trello"
    
    @fixture.test_trello_board
    @fixture.test_app
    Scenario: I can add a card
        Given I use the Trello backend
        When I go to the home page
        When I type "Add me a test card!" into the "title" box
        and I click the "Add" button
        Then I should see "Add me a test card!"

    @fixture.test_trello_board
    @fixture.test_app
    Scenario: I can add and then delete a card
        Given I use the Trello backend
        When I go to the home page
        When I type "Add me a test card!" into the "title" box
        and I click the "Add" button
        Then I should see "Add me a test card!"
        When I click the "Delete" button
        Then I should not see "Add me a test card!"