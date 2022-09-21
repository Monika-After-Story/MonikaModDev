
init python:

    dev_api_test = ""


    def dev_api_key_tester(key):
        global dev_api_test
        dev_api_test = key


    def dev_api_key_tester_error(key):
        return False, "Error Message"


    def dev_api_key_tester_returns_not_tuple(key):
        return "not tuple"


    def dev_api_key_tester_returns_not_long_enough(key):
        return ("not long enough", )


    def dev_api_key_tester_false_not_valid_error_msg(key):
        return False, 123123


    mas_registerAPIKey(
        "dev-api-key",
        "Dev Testing",
        on_change=dev_api_key_tester
    )
    mas_registerAPIKey(
        "dev-api-key-2",
        "Crash when setting",
        on_change=dev_api_key_tester_error
    )
    mas_registerAPIKey(
        "dev-api-key-3",
        "Long API KEY name for long name reasons because this wants to be long"
    )
    mas_registerAPIKey(
        "dev-api-key-4",
        "Nook Inc. Account API Token"
    )
    mas_registerAPIKey(
        "dev-api-key-not-tuple",
        "Not tuple msg logged",
        on_change=dev_api_key_tester_returns_not_tuple
    )
    mas_registerAPIKey(
        "dev-api-key-not-long-enough",
        "Short tuple msg logged",
        on_change=dev_api_key_tester_returns_not_long_enough
    )
    mas_registerAPIKey(
        "dev-api-key-not-valid-error-msg",
        "Invalid error msg type msg logged",
        on_change=dev_api_key_tester_false_not_valid_error_msg
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

