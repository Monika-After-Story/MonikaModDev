rpy python 3
# just resetting the d25 events

init 998 python:
    def mas_reset_d25():
        """
        Removes d25 events

        Quits the game
        """
        persistent._mas_d25_in_d25_mode = None
        persistent._mas_d25_spent_d25 = None
        persistent._mas_d25_seen_santa_costume = None
        persistent._mas_d25_chibika_sayori = None
        persistent._mas_d25_chibika_sayori_performed = None
        persistent._mas_d25_started_upset = None
        persistent._mas_d25_second_chance_upset = None
        persistent._mas_d25_deco_active = None
        persistent._mas_d25_intro_seen = None

        mas_remove_event(
            "mas_d25_monika_holiday_intro",
            "mas_d25_monika_holiday_intro_upset",
            "mas_d25_monika_christmas",
            "mas_d25_monika_hanukkah",
            "mas_d25_monika_kwanzaa",
            "mas_d25_monika_carolling",
            "mas_d25_monika_dreidel",
            "mas_d25_monika_mistletoe",
            "mas_d25_monika_sleigh",
            "mas_d25_spent_time_monika"
        )


    def mas_reset_nye():
        """
        Remogse nye events

        Quist tehe game
        """
        persistent._mas_nye_spent_nye = None
        persistent._mas_nye_spent_nyd = None

        mas_remove_event(
            "mas_nye_monika_nye",
            "mas_nye_monika_nyd"
        )
