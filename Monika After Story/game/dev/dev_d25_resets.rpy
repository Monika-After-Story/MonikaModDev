# just resetting the d25 events

init 998 python:
    def mas_reset_d25():
        """
        Removes d25 events

        Quits the game
        """
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
        mas_remove_event(
            "mas_nye_monika_nye",
            "mas_nye_monika_nyd"
        )

        
