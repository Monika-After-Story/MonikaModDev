
init python:

    dev_api_test = ""


    def dev_api_key_tester(key):
        global dev_api_test
        dev_api_test = key


    def dev_api_key_2_tester(key):
        return False, "Error Message"


    mas_registerAPIKey(
        "dev-api-key",
        "Dev Testing",
        on_change=dev_api_key_tester
    )
    mas_registerAPIKey(
        "dev-api-key-2",
        "Crash when setting",
        on_change=dev_api_key_2_tester
    )
    mas_registerAPIKey(
        "dev-api-key-3",
        "Long API KEY name for long name reasons because this wants to be long"
    )
    mas_registerAPIKey(
        "dev-api-key-4",
        "Nook Inc. Account API Token"
    )

    def dev_register_multipleAPI(count):
        """
        For testing - use to register a ton of api keys

        IN:
            count - number of keys to register
        """
        for x in range(count):
            mas_registerAPIKey(
                "dev-api-key-mult-{0}".format(x),
                "API Key {0}".format(x)
            )


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_api_key_tester",
            category=["dev"],
            prompt="TEST API KEY",
            pool=True,
            unlocked=True
        )
    )

label dev_api_key_tester:
    m 1eua "TIME TO TEST api key stuff"

    $ dev_key = mas_getAPIKey("dev-api-key")
    if dev_key:
        m 1eub "The api key is [dev_key]"
    else:
        m 1euc "No API key is set"

    m 1eud "The test var is set to [dev_api_test]"

    m 6wuw "Done!"
    return

