



default persistent.tempinstrument = "Инструмент"
default persistent.bday_name = "Имя"

label mas_name_cases:
    $ consonants = [u'б', u'в', u'г', u'д', u'ж', u'з', u'й', u'к', u'л', u'м', u'н', u'п', u'р', u'с', u'т', u'ф', u'х', u'ц', u'ч', u'ш', u'щ', u'ь']
    $ combinations = [u'жа', u'ша', u'ща', u'ца']
    $ combinations_abb = [u'жа', u'ша', u'ща', u'ца', u'ба', u'ва', u'ва', u'да', u'за', u'ка', u'ла', u'ма', u'на', u'па', u'ра', u'са', u'та', u'фа', u'ха', u'ча']
    $ combinations_special = [u'ка', u'ха']
    $ last_symb = player[-1:]
    $ last_symb2 = player[-2:]
    $ last_symb3 = player[-3:]
    $ last_symb_bday = persistent.bday_name[-1]
    $ last_symb2_bday = persistent.bday_name[-2:]
    $ last_symb_tempinstrument = persistent.tempinstrument[-1]
    $ last_symb2_tempinstrument = persistent.tempinstrument[-2:]
    $ last_symb3_tempinstrument = persistent.tempinstrument[-3:]
    $ mas_name_random_sistem = random.randint(1,10)











    if last_symb in consonants:
        if last_symb == u'й' or last_symb == u'ь':
            $ mas_name_what = player[:len(player)-1]+u'ю'
            $ mas_name_who = player[:len(player)-1]+u'ем'
            $ mas_name_whom = player[:len(player)-1]+u'я'
            $ mas_name_about_someone = player[:len(player)-1]+u'е'
            $ mas_name_someone = player[:len(player)-1]+u'я'
        else:
            $ mas_name_what = player+u'у'
            $ mas_name_who = player+u'ом'
            $ mas_name_whom = player+u'а'
            $ mas_name_about_someone = player+u'е'
            $ mas_name_someone = player+u'а'
    elif last_symb == 'я':
        $ mas_name_what = player[:len(player)-1]+u'и'
        $ mas_name_who = player[:len(player)-1]+u'ей'
        $ mas_name_whom = player[:len(player)-1]+u'ю'
        $ mas_name_about_someone = player[:len(player)-1]+u'е'
        $ mas_name_someone = player[:len(player)-1]+u'и'
    elif last_symb2 == 'ья':
        $ mas_name_what = player[:len(player)-1]+u'и'
        $ mas_name_who = player[:len(player)-1]+u'ёй'
        $ mas_name_whom = player[:len(player)-1]+u'ю'
        $ mas_name_about_someone = player[:len(player)-1]+u'е'
        $ mas_name_someone = player[:len(player)-1]+u'и'
    elif last_symb2 in combinations:
        $ mas_name_what = player[:len(player)-1]+u'е'
        $ mas_name_who = player[:len(player)-1]+u'ей'
        $ mas_name_whom = player[:len(player)-1]+u'у'
        $ mas_name_about_someone = player[:len(player)-1]+u'е'
        $ mas_name_someone = player[:len(player)-1]+u'и'
    elif last_symb2 in combinations_special:
        $ mas_name_what = player[:len(player)-1]+u'е'
        $ mas_name_who = player[:len(player)-1]+u'ой'
        $ mas_name_whom = player[:len(player)-1]+u'у'
        $ mas_name_about_someone = player[:len(player)-1]+u'е'
        $ mas_name_someone = player[:len(player)-1]+u'и'
    elif last_symb2 == u'ча':
        $ mas_name_what = player[:len(player)-1]+u'е'
        $ mas_name_who = player[:len(player)-1]+u'ей'
        $ mas_name_whom = player[:len(player)-1]+u'у'
        $ mas_name_about_someone = player[:len(player)-1]+u'е'
        $ mas_name_someone = player[:len(player)-1]+u'и'
    elif last_symb2 == u'иа':
        $ mas_name_what = player[:len(player)-1]+u'е'
        $ mas_name_who = player[:len(player)-1]+u'ой'
        $ mas_name_whom = player[:len(player)-1]+u'у'
        $ mas_name_about_someone = player[:len(player)-1]+u'е'
        $ mas_name_someone = player[:len(player)-1]+u'и'
    elif last_symb == u'а':
        $ mas_name_what = player[:len(player)-1]+u'е'
        $ mas_name_who = player[:len(player)-1]+u'ой'
        $ mas_name_whom = player[:len(player)-1]+u'у'
        $ mas_name_about_someone = player[:len(player)-1]+u'е'
        $ mas_name_someone = player[:len(player)-1]+u'ы'
    else:
        $ mas_name_what = player
        $ mas_name_who = player
        $ mas_name_whom = player
        $ mas_name_about_someone = player
        $ mas_name_someone = player





    if not persistent.player_abbreviated_name:
        $ player_abb = player
    else:
        if persistent.playername.lower() == "артём" or persistent.playername.lower() == "артем":
            $ player_abb = "Тём"
        elif persistent.playername.lower() == "семён" or persistent.playername.lower() == "семен":
            $ player_abb = "Сём"
        elif persistent.playername.lower() == "вероника":
            $ player_abb = "Ника"
        elif persistent.playername.lower() == "даниил" or persistent.playername.lower() == "данил":
            $ player_abb = "Дань"
        elif persistent.playername.lower() == "тимофей":
            $ player_abb = "Тим"
        elif persistent.playername.lower() == "тимур":
            $ player_abb = "Тим"
        elif persistent.playername.lower() == "алексей":
            $ player_abb = "Лёш"
        elif persistent.playername.lower() == "максим":
            $ player_abb = "Макс"
        elif persistent.playername.lower() == "дмитрий":
            $ player_abb = "Дим"
        elif persistent.playername.lower() == "сергей":
            $ player_abb = "Серёж"
        elif persistent.playername.lower() == "роман":
            $ player_abb = "Ром"
        elif persistent.playername.lower() == "ольга":
            $ player_abb = "Оль"
        elif persistent.playername.lower() == "антон":
            $ player_abb = "Антош"
        elif persistent.playername.lower() == "михаил" or persistent.playername.lower() == "миха" or persistent.playername.lower() == "мишка":
            $ player_abb = "Миш"
        elif persistent.playername.lower() == "павел":
            $ player_abb = "Паш"
        elif persistent.playername.lower() == "пётр" or persistent.playername.lower() == "петр":
            $ player_abb = "Петь"
        elif persistent.playername.lower() == "кирилл":
            $ player_abb = "Кирь"
        elif persistent.playername.lower() == "филипп":
            $ player_abb = "Филь"
        elif persistent.playername.lower() == "евгений":
            $ player_abb = "Жень"
        elif persistent.playername.lower() == "борис":
            $ player_abb = "Борь"





        elif last_symb2 in combinations_abb:
            if last_symb3 != "ика":
                $ player_abb = player[:len(player)-1]
        elif last_symb == u'я' and last_symb2 != u'ия' and last_symb2 != u'ая' and last_symb2 != u'уя' and last_symb2 != u'ея' and last_symb2 != u'оя' and last_symb2 != u'юя' and last_symb2 != u'ья':
            $ player_abb = player[:len(player)-1]+u'ь'
        elif last_symb == u'т':
            $ player_abb = player+u'ик'
        elif last_symb == u'м':
            $ player_abb = player+u'ка'
        elif last_symb == u'а':
            $ player_abb = player[:len(player)-1]+u'уля'
        else:
            $ player_abb = player




    if last_symb_bday in consonants:
        if last_symb_bday == u'й' or last_symb_bday == u'ь':
            $ mas_bday_name_whom = persistent.bday_name[:len(persistent.bday_name)-1]+u'я'
        else:
            $ mas_bday_name_whom = persistent.bday_name+u'а'
    elif last_symb_bday == 'я':
        $ mas_bday_name_whom = persistent.bday_name[:len(persistent.bday_name)-1]+u'ю'
    elif last_symb2_bday in combinations:
        $ mas_bday_name_whom = persistent.bday_name[:len(persistent.bday_name)-1]+u'у'
    elif last_symb_bday == u'а' or last_symb2_bday == u'иа':
        $ mas_bday_name_whom = persistent.bday_name[:len(persistent.bday_name)-1]+u'у'
    else:
        $ mas_bday_name_whom = persistent.bday_name




    if persistent.tempinstrument == "виолончель" or persistent.tempinstrument == "виаланчель" or persistent.tempinstrument == "виоланчель" or persistent.tempinstrument == "виалончель":
        $ mas_tempinstrument_name_whom = "виолончель"
        $ mas_tempinstrument_name_who = "виолончелью"
    elif persistent.tempinstrument == "акустическая гитара":
        $ mas_tempinstrument_name_whom = "акустическую гитару"
        $ mas_tempinstrument_name_who = "акустической гитарой"
    elif persistent.tempinstrument == "альпийский рог":
        $ mas_tempinstrument_name_whom = "альпийский рог"
        $ mas_tempinstrument_name_who = "альпийским рогом"
    elif persistent.tempinstrument == "альпийский рог":
        $ mas_tempinstrument_name_whom = "альпийский рог"
        $ mas_tempinstrument_name_who = "альпийским рогом"
    elif persistent.tempinstrument == "альтовая флейта":
        $ mas_tempinstrument_name_whom = "альтовую флейту"
        $ mas_tempinstrument_name_who = "альтовой флейтой"
    elif persistent.tempinstrument == "альтовый кларнет":
        $ mas_tempinstrument_name_whom = "альтовый кларнет"
        $ mas_tempinstrument_name_who = "альтовым кларнетом"
    elif persistent.tempinstrument == "английская гитара":
        $ mas_tempinstrument_name_whom = "английскую гитару"
        $ mas_tempinstrument_name_who = "английской гитарой"
    elif persistent.tempinstrument == "английский рожок":
        $ mas_tempinstrument_name_whom = "английский рожок"
        $ mas_tempinstrument_name_who = "английским рожком"
    elif persistent.tempinstrument == "балалайка-контрабас":
        $ mas_tempinstrument_name_whom = "балалайку-контрабас"
        $ mas_tempinstrument_name_who = "балалайкой-контрабасом"
    elif persistent.tempinstrument == "вагнеровская труба":
        $ mas_tempinstrument_name_whom = "вагнеровскую трубу"
        $ mas_tempinstrument_name_who = "вагнеровской трубой"
    elif persistent.tempinstrument == "валлийская арфа":
        $ mas_tempinstrument_name_whom = "валлийскую арфу"
        $ mas_tempinstrument_name_who = "валлийской арфой"
    elif persistent.tempinstrument == "грузинская гармонь":
        $ mas_tempinstrument_name_whom = "грузинскую гармонь"
        $ mas_tempinstrument_name_who = "грузинской гармонью"
    elif persistent.tempinstrument == "говорящий барабан":
        $ mas_tempinstrument_name_whom = "говорящий барабан"
        $ mas_tempinstrument_name_who = "говорящим барабаном"
    elif persistent.tempinstrument == "деревянная рыба":
        $ mas_tempinstrument_name_whom = "деревянную рыбу"
        $ mas_tempinstrument_name_who = "деревянной рыбой"
    elif persistent.tempinstrument == "ирландская волынка":
        $ mas_tempinstrument_name_whom = "ирландскую волынку"
        $ mas_tempinstrument_name_who = "ирландской волынкой"
    elif persistent.tempinstrument == "ирландская флейта":
        $ mas_tempinstrument_name_whom = "ирландскую флейту"
        $ mas_tempinstrument_name_who = "ирландской флейтой"
    elif persistent.tempinstrument == "классическая гитара":
        $ mas_tempinstrument_name_whom = "классическую гитару"
        $ mas_tempinstrument_name_who = "классической гитарой"
    elif persistent.tempinstrument == "колёсная лира" or tempinstrument == "колесная лира":
        $ mas_tempinstrument_name_whom = "колёсную лиру"
        $ mas_tempinstrument_name_who = "колёсной лирой"
    elif persistent.tempinstrument == "кошачье фортепиано":
        $ mas_tempinstrument_name_whom = "кошачье фортепиано"
        $ mas_tempinstrument_name_who = "кошачьим фортепиано"
    elif persistent.tempinstrument == "ливенская гармонь":
        $ mas_tempinstrument_name_whom = "ливенскую гармонь"
        $ mas_tempinstrument_name_who = "ливенской гармонью"
    elif persistent.tempinstrument == "лютневый клавесин":
        $ mas_tempinstrument_name_whom = "лютневый клавесин"
        $ mas_tempinstrument_name_who = "лютневым клавесином"
    elif persistent.tempinstrument == "молоточковое фортепиано":
        $ mas_tempinstrument_name_whom = "молоточковое фортепиано"
        $ mas_tempinstrument_name_who = "молоточковым фортепиано"
    elif persistent.tempinstrument == "народная скрипка":
        $ mas_tempinstrument_name_whom = "народную скрипку"
        $ mas_tempinstrument_name_who = "народной скрипкой"
    elif persistent.tempinstrument == "охотничий рог":
        $ mas_tempinstrument_name_whom = "охотничий рог"
        $ mas_tempinstrument_name_who = "охотничим рогом"
    elif persistent.tempinstrument == "пастушетская труба":
        $ mas_tempinstrument_name_whom = "пастушетскую трубу"
        $ mas_tempinstrument_name_who = "пастушетской трубой"
    elif persistent.tempinstrument == "поперечная флейта":
        $ mas_tempinstrument_name_whom = "поперечную флейту"
        $ mas_tempinstrument_name_who = "поперечной флейтой"
    elif persistent.tempinstrument == "португальская гитара":
        $ mas_tempinstrument_name_whom = "португальскую гитару"
        $ mas_tempinstrument_name_who = "португальской гитарой"
    elif persistent.tempinstrument == "пятиструнная скрипка":
        $ mas_tempinstrument_name_whom = "пятиструнную скрипку"
        $ mas_tempinstrument_name_who = "пятиструнной скрипкой"
    elif persistent.tempinstrument == "русская семиструнная гитара":
        $ mas_tempinstrument_name_whom = "русскую семиструнную гитару"
        $ mas_tempinstrument_name_who = "русской семиструнной гитарой"
    elif persistent.tempinstrument == "саратовская гармонь":
        $ mas_tempinstrument_name_whom = "саратовскую гармонь"
        $ mas_tempinstrument_name_who = "саратовской гармонью"
    elif persistent.tempinstrument == "символический орган":
        $ mas_tempinstrument_name_whom = "символический орган"
        $ mas_tempinstrument_name_who = "символическим органом"
    elif persistent.tempinstrument == "скрипка штроха" or tempinstrument == "скрипка Штроха":
        $ mas_tempinstrument_name_whom = "скрипку Штроха"
        $ mas_tempinstrument_name_who = "скрипкой Штроха"
    elif persistent.tempinstrument == "стальной барабан":
        $ mas_tempinstrument_name_whom = "стальной барабан"
        $ mas_tempinstrument_name_who = "стальным барабаном"
    elif persistent.tempinstrument == "стиральная доска":
        $ mas_tempinstrument_name_whom = "стиральную доску"
        $ mas_tempinstrument_name_who = "стиральной доской"
    elif persistent.tempinstrument == "теноровый барабан":
        $ mas_tempinstrument_name_whom = "теноровый барабан"
        $ mas_tempinstrument_name_who = "теноровым барабаном"
    elif persistent.tempinstrument == "флейта пана" or tempinstrument == "флейта Пана":
        $ mas_tempinstrument_name_whom = "флейту Пана"
        $ mas_tempinstrument_name_who = "флейтой Пана"
    elif persistent.tempinstrument == "флейта-пикколо":
        $ mas_tempinstrument_name_whom = "флейту-пикколо"
        $ mas_tempinstrument_name_who = "флейтой-пикколо"
    elif persistent.tempinstrument == "четвертитоновый кларнет":
        $ mas_tempinstrument_name_whom = "четвертитоновый кларнет"
        $ mas_tempinstrument_name_who = "четвертитоновыс кларнетом"
    elif persistent.tempinstrument == "щелевой барабан":
        $ mas_tempinstrument_name_whom = "щелевой барабан"
        $ mas_tempinstrument_name_who = "щелевым барабаном"
    elif persistent.tempinstrument == "кости":
        $ mas_tempinstrument_name_whom = persistent.tempinstrument
        $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ями'




    elif last_symb_tempinstrument in consonants:
        if last_symb3_tempinstrument == u'яль':
            $ mas_tempinstrument_name_whom = persistent.tempinstrument
            $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ем'
        elif last_symb3_tempinstrument == u'ики' or persistent.tempinstrument == "ложки":
            $ mas_tempinstrument_name_whom = persistent.tempinstrument
            $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ами'
        elif last_symb2_tempinstrument == u'ок':
            $ mas_tempinstrument_name_whom = persistent.tempinstrument
            $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-2]+u'ком'
        elif last_symb_tempinstrument == u'ь':
            $ mas_tempinstrument_name_whom = persistent.tempinstrument
            $ mas_tempinstrument_name_who = persistent.tempinstrument+u'ю'
        elif last_symb_tempinstrument == u'й':
            $ mas_tempinstrument_name_whom = persistent.tempinstrument
            $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ем'
        else:
            $ mas_tempinstrument_name_whom = persistent.tempinstrument
            $ mas_tempinstrument_name_who = persistent.tempinstrument+u'ом'
    elif last_symb_tempinstrument == 'я':
        $ mas_tempinstrument_name_whom = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ю'
        $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ей'
    elif last_symb2_tempinstrument in combinations:
        $ mas_tempinstrument_name_whom = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'у'
        $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ей'
    elif last_symb_tempinstrument == u'а' or last_symb2_tempinstrument == u'иа':
        $ mas_tempinstrument_name_whom = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'у'
        $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ой'
    elif last_symb_tempinstrument == u'ы':
        $ mas_tempinstrument_name_whom = persistent.tempinstrument
        $ mas_tempinstrument_name_who = persistent.tempinstrument[:len(persistent.tempinstrument)-1]+u'ами'
    else:
        $ mas_tempinstrument_name_whom = persistent.tempinstrument
        $ mas_tempinstrument_name_who = persistent.tempinstrument

