# emergency dumping file

<<<<<<< HEAD
init 3000 python:
=======
init 999 python:
>>>>>>> be423abed5eb988f07d48c189406ae8a9bccd9f5
    # outfiles
    outtext = (
        "mrt: {0}\nmerr: {1}\nmmrh: {2}\nrs: {3}\n"
    )
<<<<<<< HEAD
    basedir = config.basedir.replace("\\", "/")
    with open(basedir + "/dumps.log", "w") as dump_file:
        dump_file.write(outtext.format(
            len(monika_random_topics),
            persistent._mas_enable_random_repeats,
            persistent._mas_monika_repeated_herself,
            persistent.random_seen
        )
    )
    del outtext
=======
#    basedir = config.basedir.replace("\\", "/")
#    with open(basedir + "/dumps.log", "w") as dump_file:
#        dump_file.write(outtext.format(
#            len(monika_random_topics),
#            persistent._mas_enable_random_repeats,
#            persistent._mas_monika_repeated_herself,
#            persistent.random_seen
#        )
#    )
#    del outtext
>>>>>>> be423abed5eb988f07d48c189406ae8a9bccd9f5

